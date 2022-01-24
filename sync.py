from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from dotenv import load_dotenv
from includes import api_simkl
from fuzzywuzzy import fuzz
import os, sys, requests

load_dotenv()
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
SERVERNAME = os.environ.get("SERVERNAME")
TOKENBASED = os.environ.get("TOKENBASED")
BASEURL = os.environ.get("BASEURL")
TOKEN = os.environ.get("TOKEN")

try:
    if TOKENBASED:
        print("Logging in using token")
        plex = PlexServer(BASEURL, TOKEN)
    else:
        print("Logging in using Username/password")
        account = MyPlexAccount(USERNAME, PASSWORD)
        plex = account.resource(SERVERNAME).connect()  # returns a PlexServer instance
    print("Logged in")
except:
    sys.exit("Failed to login")

api = api_simkl.Simkl()

allItems = api.get_all_items()

print()

movies = plex.library.section('Movies')
for video in movies.search(unwatched=True):
    for watched in allItems["movies"]:
        if video.title in watched["movie"]["title"]:
            print(video.title, " matched ", watched["movie"]["title"])
            video.markWatched()

shows = plex.library.section('Series')
for video in shows.search(unwatched=True):
    for watched in allItems["shows"]:
        if video.title in watched["show"]["title"]:
            print(video.title, " matched ", watched["show"]["title"])
            video.markWatched()
