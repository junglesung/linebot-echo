from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('SjtzxUrFzMtJA074sK6HZvkxFKp6BfewjrQMroDZ++hqwT+W9Zf37C/bJLAgQzXRm2ooSAKFmLzNg6G8PC9B/NeE91Er4/eQItxBhvv8YocEq7c+0/kqbhQ8q0mT0es9sTrgpdcD7Dwk6iEXgIFhcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1fe3235aef7d160e249ec58405fd9542')


@app.route("/callback", methods=['POST'])
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()