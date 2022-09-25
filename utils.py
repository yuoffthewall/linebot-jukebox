import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, ButtonsTemplate, MessageTemplateAction, URITemplateAction, ImageSendMessage, CarouselTemplate, CarouselColumn
from dotenv import load_dotenv

load_dotenv()
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(id, title, text, options):
    my_actions = []
    for option in options:
        my_actions.append( MessageTemplateAction(label=option, text=option) )
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://play-lh.googleusercontent.com/zim-eMjkFdDeXUKv1dLiFuWgsUvy1cIdAJbOJDY7pg1P27A0TdyWxRXv1v0AO4Vn9gg',
            title=title,
            text=text,
            actions=my_actions
        )
    )

    line_bot_api.push_message(id, message)
    return "OK"

def send_image_carousel(id, options):
    cols = []
    for option in options:
        cols.append(
            ImageCarouselColumn(
                image_url=option['icons'][0]['url'],
                action=MessageTemplateAction(
                    label=option['name'],
                    text=option['id'],
                )
            )
        )
    message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(columns=cols)
    )
    line_bot_api.push_message(id, message)
    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
