myid='21pms7hjn5mfszuxggxdzlgcy'

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

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

def search_aritst_top_tracks(artist):
	results = sp.artist_top_tracks(artist)
	msg = ""
	tracklist = []
	for track in results['tracks']:
		msg = msg+track['name']+'\n'
		print(track['name'])
		tracklist.append(track['uri'])

def create_playlist():
	playlist = sp.user_playlist_create(myid, "test", public=False)
	sp.user_playlist_add_tracks(myid, playlist['id'], tracklist)

def search(search_str, type):
	result = sp.search(search_str, type=type)
	return result['artists']['items']

def search_artist(artist_id):
	result = sp.artist(artist_id)

def get_categories():
	result = sp.categories()
	return result['categories']['items']


if __name__ == '__main__':
	result = sp.categories()
	print(json.dumps(result, indent=4))
