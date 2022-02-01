import spotipy
from bs4 import BeautifulSoup
import requests

# allows you to create private playlists
scope = "playlist-modify-private"

# token
Oauth = spotipy.SpotifyOAuth(
    scope=scope, 
    redirect_uri="http://example.com",
    cache_path=".cache"
)

# speetyspooty object
sp = spotipy.Spotify(auth_manager=Oauth)

# ask what year to get music from
year = input("please enter year to get music from (YYYY): ")
user = sp.current_user()["id"]

# create the playlist
playlist = sp.user_playlist_create(user=user, name=f"Top Songs of {year}", public=False, description=f"top songs from the year {year}")

# get the wiki site with the corresponding year
site = requests.get(f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}")
soup = BeautifulSoup(site.text, "html.parser")

# get the 100 rows of the list
rows = soup.find_all(name="tr")[1:100]
songs = []
for row in rows:
    # each row has 3 cells
    cells = row.find_all("td")
    song = cells[1].getText().strip("\"")
    artist = cells[2].getText().strip("\"")

    search = sp.search(q=f"track:{song} artist:{artist} year:{year}", type="track")

    try:
        # uri of the song
        current_song = search["tracks"]["items"][0]["uri"]

        # add the song's uri
        songs.append(current_song)
    except IndexError:
        print(f"{song} = bad song dont ever listen to it")

# add all the songs to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=songs)