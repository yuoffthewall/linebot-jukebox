from transitions.extensions import GraphMachine

from utils import send_text_message


class setMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_goto_options(self, event):
        text = event.message.text
        return text.lower() == "drop some good shit"

    def is_goto_vibes(self, event):
        text = event.message.text
        return text.lower() == "ord"

    def on_enter_order_vibes(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
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
        states=["initial", "options", "vibes", "artists", "order_vibes", "order_artists"],
        transitions=[
            {
                "trigger": "move",
                "source": "initial",
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
                "source": ["vibes", "artists"],
                "dest": "initial",
            },
            {
				"trigger": "go_back", 
				"source": ["options", "vibes", "artists"], 
				"dest": "initial",
			},
        ],
        initial="initial",
        auto_transitions=False,
        show_conditions=True,
    )
