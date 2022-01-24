import requests, os, time

from dotenv import load_dotenv
load_dotenv()

BASEURL = os.environ.get("BASEURL")
SIMKLCLIENTID = os.environ.get("SIMKLCLIENTID")
SIMKLCLIENTSECRET = os.environ.get("SIMKLCLIENTSECRET")

r = requests.get(f'https://api.simkl.com/oauth/pin?client_id={SIMKLCLIENTID}&redirect=127.0.0.1')

json = r.json()

print("user code: ", json["user_code"])
os.system(f"xdg-open 'https://simkl.com/pin/'")

r = requests.get(f'https://api.simkl.com/oauth/pin/{json["user_code"]}?client_id={SIMKLCLIENTID}')

while r.json()["result"] != "OK":
    print(r.json())
    time.sleep(5)
    r = requests.get(f'https://api.simkl.com/oauth/pin/{json["user_code"]}?client_id={SIMKLCLIENTID}')

print("SIMKLAPITOKEN: ", r.json()["access_token"])
