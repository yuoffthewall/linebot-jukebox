from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message, send_image_carousel
import spotify as sp

class setMachine(GraphMachine):
	def __init__(self, **machine_configs):
		self.machine = GraphMachine(model=self, **machine_configs)

	def is_goto_ask(self, event):
		return True
	
	def on_enter_ask(self, event):
		title = "DJ linebot in the house"
		text = "Got some good shit here. You want some?"
		send_button_message(event.source.user_id, title, text, ["Hell yeah", "Nah, thanks"])	

	def is_goto_options(self, event):
		text = event.message.text
		return text.lower() == "hell yeah"

	def on_enter_options(self, event):
		title = "Here's the order options!"
		text = "You can order songs accroding to artists, vibes or songs."
		send_button_message(event.source.user_id, title, text, ["artists", "vibes", "songs"])	

	def is_goto_vibes(self, event):
		text = event.message.text
		return text.lower() == "vibes"

	def on_enter_vibes(self, event):
		options = ['hiphop', 'rock', 'rnb']
		results = sp.get_categories(options)
		send_image_carousel(event.source.user_id, results)	
	
	def on_exit_vibes(self, event):
		category = event.message.text
		list_id = sp.get_catagory_playlists(category)[1]
		tracks = sp.get_playlist_tracks(list_id)[:30]
		sp.create_playlist(sp.myid, tracks)


	def is_goto_artists(self, event):
		text = event.message.text
		return text.lower() == "artists"

	def on_enter_artists(self, event):
		msg = "Please give me the artists list.\nOne artist per line."
		send_text_message(event.reply_token, msg)

	def on_exit_artists(self, event):
		names = event.message.text.split("\n")
		artists = []
		for name in names:
			artist = sp.search(name, type="artist")['artists']['items'][0]['id']
			artists.append(artist)

		tracks = []
		for artist in artists:
			tracks += sp.search_aritst_top_tracks(artist)
		sp.create_playlist(sp.myid, tracks)
		
		

	def is_goto_songs(self, event):
		text = event.message.text
		return text.lower() == "songs"

	def on_enter_songs(self, event):
		msg = "Please give me the artists list.\nOne artist per line."
		send_text_message(event.reply_token, msg)

	def on_exit_songs(self, event):
		names = event.message.text.split("\n")
		tracks = []
		for name in names:
			track = sp.search(name, type="track")['tracks']['items'][0]['id']
			tracks.append(track)
		sp.create_playlist(sp.myid, tracks)
	
	def is_invalid(self, event):
		if self.state == 'ask':
			return not self.is_goto_options(event)
		elif self.state == 'options':
			options = ['vibes', 'artists', 'songs']
			return options.count(event.message.text) == 0
		elif self.state == 'vibes':
			options = ['hiphop', 'rock', 'rnb']
			return options.count(event.message.text) == 0

	def on_enter_state2(self, event):
		print("I'm entering state2")

		reply_token = event.reply_token
		send_text_message(reply_token, "Trigger state2")
		self.go_back()



def create_machine():
	machine = setMachine(
		states=["initial", "ask", "options", "vibes", "artists", "songs"],
		transitions=[
			{
				"trigger": "move",
				"source": "initial",
				"dest": "ask",
				"conditions": "is_goto_ask",
			},
			{
				"trigger": "move",
				"source": "ask",
				"dest": "options",
				"conditions": "is_goto_options",
			},
			{
				"trigger": "move",
				"source": "options",
				"dest": "vibes",
				"conditions": "is_goto_vibes",
			},
			{
				"trigger": "move",
				"source": "options",
				"dest": "artists",
				"conditions": "is_goto_artists",
			},
			{
				"trigger": "move",
				"source": "options",
				"dest": "songs",
				"conditions": "is_goto_songs",
			},
			{
				"trigger": "move",
				"source": ["ask", "options", "vibes"],
				"dest": "=",
				"conditions": "is_invalid",
			},
			{
				"trigger": "move",
				"source": ["artists", "songs", "vibes"],
				"dest": "ask",
			},
			{
				"trigger": "go_back", 
				"source": ["ask", "options", "vibes", "artists", "songs"], 
				"dest": "initial",
			},
		],
		initial="initial",
		auto_transitions=False,
		show_conditions=True,
	)
	return machine
