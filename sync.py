from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from dotenv import load_dotenv
from includes import api_simkl
from fuzzywuzzy import fuzz

from includes import anilist
from includes import graphql
import os, sys, requests

load_dotenv()
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
SERVERNAME = os.environ.get("SERVERNAME")
TOKENBASED = os.environ.get("TOKENBASED")
BASEURL = os.environ.get("BASEURL")
TOKEN = os.environ.get("TOKEN")
ANILISTCLIENTID = os.environ.get("ANILISTCLIENTID")
ANILISTCLIENTSECRET = os.environ.get("ANILISTCLIENTSECRET")
GRAPHQLTOKEN = os.environ.get("GRAPHQLTOKEN")

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
# The code underneath is a buildingblock that can be reused as seen below. change the values where needed
# movies = plex.library.section('LibraryName, as seen below')
# for video in movies.search(unwatched=True):
#     for watched in allItems["movies"]:
#         if video.title.lower() == watched["movie"]["title"].lower():
#             print(video.title, " matched ", watched["movie"]["title"])
#             video.markWatched()

# Examples
movies = plex.library.section('Movies')
for video in movies.search(unwatched=True):
    for watched in allItems["movies"]:
        if video.title.lower() == watched["movie"]["title"].lower():
            print(video.title, " matched ", watched["movie"]["title"])
            video.markWatched()

shows = plex.library.section('Series')
for video in shows.search(unwatched=True):
    for watched in allItems["shows"]:
        if video.title.lower() in watched["show"]["title"].lower():
            print(video.title, " matched ", watched["show"]["title"])
            video.markWatched()


graphql.ANILIST_ACCESS_TOKEN = GRAPHQLTOKEN
# url = f"https://anilist.co/api/v2/oauth/authorize?client_id={ANILISTCLIENTID}&response_type=token"
# print(url)
anilist_series = anilist.process_user_list("Fenroar")

#Example of an anime library
anime = plex.library.section('Anime')
for video in anime.search(unwatched=True):
    for series in anilist_series:
        if series.status == "COMPLETED":
            if series.title_english:
                if video.title.lower() in series.title_english.lower().replace(":",""):
                    print(video.title, " matched ", series)
                    video.markWatched()
            elif series.title_romaji:
                if video.title.lower() in series.title_romaji.lower().replace(":",""):
                    print(video.title, " matched ", series)
                    video.markWatched()
            elif series.synonyms:
                if video.title.lower() in series.synonyms.lower().replace(":",""):
                    print(video.title, " matched ", series)
                    video.markWatched()
