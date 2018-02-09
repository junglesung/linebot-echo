# coding=utf-8

# Standard libraries
import logging
import time

# Third-party libraries
from flask import Flask, request, abort
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    CarouselColumn,
    CarouselTemplate,
    URITemplateAction,
    TemplateSendMessage
)

# Constants
BACKEND_SERVICE = 'http://35.229.156.92:7705'

# Variables
app = Flask(__name__)

# Replace by your channel secret and access token from Line Developers console -> Channel settings.
LINE_CHANNEL_ACCESS_TOKEN = 'SjtzxUrFzMtJA074sK6HZvkxFKp6BfewjrQMroDZ++hqwT+W9Zf37C/bJLAgQzXRm2ooSAKFmLzNg6G8PC9B/NeE91Er4/eQItxBhvv8YocEq7c+0/kqbhQ8q0mT0es9sTrgpdcD7Dwk6iEXgIFhcgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '1fe3235aef7d160e249ec58405fd9542'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Reply the same words if the message is short
    if len(event.message.text.lower()) <= 2:
        line_bot_echo(event)
    else:
        line_bot_car_suggestion_process(event)


def line_bot_car_suggestion_process(event):
    # Get user data
    user_info = event.source.user_id
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name

    # Build the message to send to backend
    time_log = time.strftime("%Y-%m-%d %H:%M:%S")
    json_data = {'data': {'message_raw': event.message.text.replace('\n', ' '),
                          'user_data': {'user_id': user_info,
                                        'time_log': time_log,
                                        'display_name': display_name}}}
    headers = {'Content-Type': 'application/json'}
    url = BACKEND_SERVICE + '/api/v1/car-suggestion'
    try:
        result = requests.post(url=url, json=json_data, headers=headers)
        result.encoding = 'utf-8'
        result = result.json()
        line_bot_car_suggestion_response(event, result)
    except Exception as exc:
        logging.exception('Connect to backend server %s error: %s', url, exc)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='連線中斷，請再重新嘗試一次!'))


def line_bot_car_suggestion_response(event, result):
    # Check response status
    status = result.get('status')
    if status is None or status != 'ok':
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='抱歉目前無法找到適合您的商品~\n請更加詳細描述您的手機購買需求!'))
        return
    # Build a Carousel message
    columns_data = []
    for p in result['products']:
        image_url = p['photo']
        title = '%s %s' % (p['brand'], p['name'])
        price = '價格 $ %s - %s 萬' % (str(p['min_price']), str(p['max_price']))
        action_intro = URITemplateAction(label='詳細資料', uri=p['introduction'])
        carousel_obj = CarouselColumn(thumbnail_image_url=image_url,
                                      title=title,
                                      text=price,
                                      actions=[action_intro])
        columns_data.append(carousel_obj)
        # Check maximum 10 columns limited by Line
        if len(columns_data) >= 10:
            break
    message = TemplateSendMessage(alt_text='您的推薦結果',
                                  template=CarouselTemplate(columns=columns_data,
                                                            imageSize='contain'))
    # Reply message
    line_bot_api.reply_message(event.reply_token, message)


def line_bot_echo(event):
    # Replace the text by what you want to say
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
