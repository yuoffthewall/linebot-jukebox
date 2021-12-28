from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message, send_image_carousel
import spotify as sp

class setMachine(GraphMachine):
	def __init__(self, **machine_configs):
		self.machine = GraphMachine(model=self, **machine_configs)
		self.link = ''
		self.vibes = ['hiphop', 'chill', 'rock', 'rnb', 'kpop', 'at_home', 'party']

	'''
	def is_goto_initial(self, event):
		return True

	def on_enter_initial(self, event):
		text = "Please provide your spotify id to get started!"
		send_text_message(event.reply_token, text)

	def is_goto_ask(self, event):
		self.user_id = event.message.text
		try:
			result = sp.sp.user(self.user_id)
		except:
			send_text_message(event.reply_token, "Invalid id!\n"+
					"Please provide your spotify id to get started!")
			return False
		return True
	'''
	def is_goto_ask(self, event):
		return True
	
	def on_enter_ask(self, event):
		title = "DJ linebot in the house"
		text = "Got some good shit here. You want some?"
		send_button_message(event.source.user_id, title, text, ["Hell yeah!", "Nah, thanks"])	


	def is_goto_options(self, event):
		text = event.message.text
		return text.lower() == "hell yeah!"

	def on_enter_options(self, event):
		title = "Here's the order options!"
		text = "You can order tracks accroding to artists, vibes or tracks."
		send_button_message(event.source.user_id, title, text, ["vibes", "artists", "tracks"])	


	def is_goto_vibes(self, event):
		text = event.message.text
		return text.lower() == "vibes"

	def on_enter_vibes(self, event):
		results = sp.get_categories(self.vibes)
		send_image_carousel(event.source.user_id, results)	

	def valid_vibes(self, event):
		return self.vibes.count(event.message.text) > 0
	
	def on_exit_vibes(self, event):
		if not self.valid_vibes(event):
			send_text_message(event.reply_token, "Invalid choice!")
			return
		category = event.message.text
		list_id = sp.get_catagory_playlists(category)[0]
		tracks = sp.get_playlist_tracks(list_id)[:30]
		playlist = sp.create_playlist(sp.user_id, tracks)
		self.link = playlist['external_urls']['spotify']
		self.send_link(event)


	def is_goto_artists(self, event):
		text = event.message.text
		return text.lower() == "artists"

	def on_enter_artists(self, event):
		msg = ("Please give me the artists list.\nOne artist per line.\n"+
				"For example:\n\nKendrick Lamar\nTravis scott\nJay Chou")
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
		playlist = sp.create_playlist(sp.user_id, tracks)
		self.link = playlist['external_urls']['spotify']
		self.send_link(event)
		
		

	def is_goto_songs(self, event):
		text = event.message.text
		return text.lower() == "tracks"

	def on_enter_songs(self, event):
		msg = ("Please give me the tracks list.\nOne track per line.\n"+
				"For example:\n\nHumble\nDNA\nMoney Trees")
		send_text_message(event.reply_token, msg)

	def on_exit_songs(self, event):
		names = event.message.text.split("\n")
		tracks = []
		for name in names:
			track = sp.search(name, type="track")['tracks']['items'][0]['id']
			tracks.append(track)
		playlist = sp.create_playlist(sp.user_id, tracks)
		self.link = playlist['external_urls']['spotify']
		self.send_link(event)
	
	def is_invalid(self, event):
		if self.state == 'ask':
			return not self.is_goto_options(event)
		elif self.state == 'options':
			options = ['vibes', 'artists', 'tracks']
			return options.count(event.message.text) == 0
		elif self.state == 'vibes':
			return self.vibes.count(event.message.text) == 0

	def send_link(self, event):
		text = ("Your daily mix has been created!\n"+
				"here's the link:\n"+
				self.link)
		send_text_message(event.reply_token, text)

	'''
	def on_enter_state2(self, event):
		print("I'm entering state2")

		reply_token = event.reply_token
		send_text_message(reply_token, "Trigger state2")
		self.go_back()
	'''

def create_machine():
	machine = setMachine(
		states=["user", "ask", "options", "vibes", "artists", "songs"],
		transitions=[
			{
				"trigger": "move",
				"source": "user",
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
				"source": "vibes",
				"dest": "ask",
				"conditions": "valid_vibes",
			},
			{
				"trigger": "move",
				"source": ["ask", "options", "vibes"],
				"dest": "=",
				"conditions": "is_invalid",
			},
			{
				"trigger": "move",
				"source": ["artists", "songs"],
				"dest": "ask",
			},
			{
				"trigger": "invalid",
				"source": ["ask", "options", "vibes"],
				"dest": "=",
			},
			{
				"trigger": "go_back", 
				"source": ["ask", "options", "vibes", "artists", "songs"], 
				"dest": "initial",
			},
		],
		initial="user",
		auto_transitions=False,
		show_conditions=True,
	)
	return machine
