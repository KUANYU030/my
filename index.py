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

line_bot_api = LineBotApi('xkA8wRclAU/HE4FFvj6M1iS0wZFuc2w1s5tNtpyD61Q7cwTo+vK5PhhS9HDdjy1bEqEBeScV9eU78iZBStGsUwurS2H5U2sKeC1bDhJ8ssvFBWTQfI6/G2ZNXLraMYIrk537TNr6V9bbP6rfN0DYFQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dff00609107715ef6cf4ba0404fd7828')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
