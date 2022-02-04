# ReverseSyncPlex

A tool to sync FROM sites such as Anilist and Simkl TO plex. This is handy when Plex was reinstalled and you lost your progress.

At the moment this is very finicky, as you need to change the code yourself alot,  but I tried to make it a s clear as possible.

Open sync.py and edit the following:
- line 38-43 (the for loop) is a copy-paste example of a library in plex. more information inside the file.
- line 64: Change "Fenroar" to your anilist username

example .env file (create this in root folder):
```
#Choose if you want to use the token (true) (faster, but you'll need to refresh the token) or the credential (false) (slower but easier) method
TOKENBASED=TRUE
#The url to your plex server, internal ip is faster
BASEURL='http://yourplexserverip:32400'
#plex credentials
USERNAME='yourplexusername'
PASSWORD='plexpassword'
#Name of your plex server
SERVERNAME='SHIELD Android TV'
#extract this token like this: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
TOKEN='<TOKEN>'
#Create a simkl app here: https://simkl.com/settings/developer/add/
SIMKLCLIENTID='yourclientid'
SIMKLCLIENTSECRET='yourclientsecret'
#this is a bit weird, set your redirect uri in the cimkl app to "127.0.0.1", and execute "python includes/getSimklToken.py". While this runs, you will get a user-token. Go to https://simkl.com/pin/ and fill in that token. There will be an error, but the code should print the access token.
SIMKLAPITOKEN='yourapitoken'
#create an app here: https://anilist.co/settings/developer
ANILISTCLIENTID='yourid'
ANILISTCLIENTSECRET='yoursecret'
#go to "https://anilist.co/api/v2/oauth/authorize?client_id={ANILISTCLIENTID}&response_type=token" (replace your anilistclientid in the url) and you should get the token
GRAPHQLTOKEN="yourtokenhere"
```
