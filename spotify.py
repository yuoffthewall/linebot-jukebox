import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyImplicitGrant, SpotifyPKCE
from dotenv import load_dotenv
import json

load_dotenv()
Client_id = os.getenv("Client_id", None)
Client_secret = os.getenv("Client_secret", None)
Redirect_uri = os.getenv("Redirect_uri", None)
user_id = os.getenv("User_id", None)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_id,
                                               client_secret=Client_secret,
                                               redirect_uri=Redirect_uri,
                                               scope="user-library-read playlist-modify-private playlist-modify-public"))

def show_my_tracks():
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])

#
def search_aritst_top_tracks(artist):
    results = sp.artist_top_tracks(artist)
    msg = ""
    tracklist = []
    for track in results['tracks'][:10]:
        msg = msg+track['name']+'\n'
        print(track['name'])
        tracklist.append(track['uri'])
    return tracklist

#
def create_playlist(user_id, tracks):
    playlist = sp.user_playlist_create(user_id, "dailyMix", public=True, collaborative=False)
    sp.user_playlist_add_tracks(user_id, playlist['id'], tracks)
    return playlist

#
def search(search_str, type):
    result = sp.search(search_str, type=type)
    return result

def search_artist(artist_id):
    result = sp.artist(artist_id)

#
def get_categories(options):
    results = sp.categories(limit=50, country='US')['categories']['items']
    info = []
    count = 0;
    for result in results:
        name = result['name']
        if options.count(name) > 0:
            info.append(result)
            count+=1
        if count == len(options): break

    return info

#
def get_catagory_playlists(category):
    result = sp.category_playlists(category, country='US')
    list_ids = []
    for playlist in result['playlists']['items']:
        list_ids.append(playlist['id'])
    return list_ids

#
def get_playlist_tracks(playlist):
    result = sp.playlist(playlist, fields='tracks')['tracks']['items']
    tracks = []
    for item in result:
        tracks.append(item['track']['uri'])
    return tracks

if __name__ == '__main__':
    result = sp.categories()
