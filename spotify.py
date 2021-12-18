myid='21pms7hjn5mfszuxggxdzlgcy'

import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json

load_dotenv()
Client_id = os.getenv("Client_id", None)
Client_secret = os.getenv("Client_secret", None)
Redirect_uri = os.getenv("Redirect_uri", None)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_id,
                                               client_secret=Client_secret,
                                               redirect_uri=Redirect_uri,
                                               scope="user-library-read playlist-modify-private"))
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
	for track in results['tracks'][:5]:
		msg = msg+track['name']+'\n'
		print(track['name'])
		tracklist.append(track['uri'])
	return tracklist

#
def create_playlist(user_id, tracks):
	playlist = sp.user_playlist_create(user_id, "test", public=False)
	sp.user_playlist_add_tracks(user_id, playlist['id'], tracks)

#
def search(search_str, type):
	result = sp.search(search_str, type=type)
	return result

def search_artist(artist_id):
	result = sp.artist(artist_id)

#
def get_categories():
	result = sp.categories()
	return result['categories']['items']

#
def get_catagory_playlists(category):
	result = sp.category_playlists(category)
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
	list_id = get_catagory_playlists("rock")[1]
	result = get_playlist_tracks(list_id)
	#print(result)
	print(json.dumps(result, indent=4))
