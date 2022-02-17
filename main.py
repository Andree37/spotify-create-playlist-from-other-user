from dataclasses import fields
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

the_sounds_of_spotify_user = "thesoundsofspotify"
# Add your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET to the environment variables
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
scope = "playlist-modify-public"
my_sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


playlist_name = "Mixordiaa"
playlist_id = None

# create spotify playlist if not exists
my_playlists_results = my_sp.current_user_playlists()
found = False
for item in my_playlists_results["items"]:
    if playlist_name == item["name"]:
        found = True
        playlist_id = item["id"]
        break

if not found:
    user_id = sp.me()["id"]
    d = my_sp.user_playlist_create(user_id, playlist_name)
    playlist_id = d["id"]


# variables for filtering playlists

name_check = "The Sound of"
offset = 0
n_genres = 6325  # upper bound to reflect the n of playlists the user has


while offset < n_genres:
    playlists = sp.user_playlists(the_sounds_of_spotify_user, limit=50, offset=offset)
    items_to_add = []

    for playlist in playlists["items"]:
        if (
            name_check in playlist["name"]
            and playlist["name"] != "The Sound of Everything"
        ):
            id = playlist["id"]
            results = sp.playlist(id, fields="tracks")
            first_track = results["tracks"]["items"][0]
            track = first_track["track"]
            track_id = track["id"]
            items_to_add.append(track_id)
            print("To add: ", track_id)
    offset += 50

    my_sp.playlist_add_items(playlist_id=playlist_id, items=items_to_add)
    print("Added ", len(items_to_add), "new tracks")
