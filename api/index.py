import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from api.chatgpt import ChatGPT

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.msg_list.append("Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people! Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.\nUser: ")
    
    def add_msg(self, new_msg):
        if len(self.msg_list) >= 10:
            self.remove_msg()
        self.msg_list.append(new_msg)

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0.8))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 2048))

    def get_response(self):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.prompt.generate_prompt(),
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            max_tokens=self.max_tokens
        )
        return response['choices'][0]['text'].strip()

    def add_msg(self, text):
        self.prompt.add_msg(text)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    if event.message.text == "デジタク起きて！":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="おはよう！ ^_^ "))
        return

    if event.message.text == "デジタク休んで！":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="わかった！ > <，用事がある時、「デジタク起きて！」送ってね > <"))
        return

    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("デジタク:", "", 1)
        chatgpt.add_msg(f"デジタク:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

if __name__ == "__main__":
    app.run()
