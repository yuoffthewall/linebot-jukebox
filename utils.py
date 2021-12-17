import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, ButtonsTemplate, MessageTemplateAction, URITemplateAction, ImageSendMessage, CarouselTemplate, CarouselColumn


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(id, options):
	my_actions = []
	for option in options:
		my_actions.append( MessageTemplateAction(label=option, text=option) )
	message = TemplateSendMessage(
		alt_text='Buttons template',
		template=ButtonsTemplate(
			thumbnail_image_url='https://example.com/image.jpg',
			title='Menu',
			text='Please select',
			actions=my_actions
		)
	)

	line_bot_api.push_message(id, message)
	return "OK"
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
