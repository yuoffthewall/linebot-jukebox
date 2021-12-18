from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message
import spotify as sp

class setMachine(GraphMachine):
	def __init__(self, **machine_configs):
		self.machine = GraphMachine(model=self, **machine_configs)

	def is_goto_ask(self, event):
		return True
	
	def on_enter_ask(self, event):
		send_button_message(event.source.user_id, ["Hell yeah", "Nah, thanks"])	

	def is_goto_options(self, event):
		text = event.message.text
		return text.lower() == "hell yeah"

	def on_enter_options(self, event):
		send_button_message(event.source.user_id, ["artists", "vibes", "songs"])	

	def is_goto_vibes(self, event):
		text = event.message.text
		return text.lower() == "vibes"

	def on_enter_vibes(self, event):
		send_button_message(event.source.user_id, ["hiphop", "rock"])	

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


		reply_token = event.reply_token
		send_text_message(reply_token, "Trigger state1")
		#self.go_back()

	def on_exit_vibes(self):
		print("Leaving state1")

	def on_enter_state2(self, event):
		print("I'm entering state2")

		reply_token = event.reply_token
		send_text_message(reply_token, "Trigger state2")
		self.go_back()

	def on_exit_state2(self):
		print("Leaving state2")


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
				"after": "repeat",
			},
			{
				"trigger": "move",
				"source": ["artists", "songs"],
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
