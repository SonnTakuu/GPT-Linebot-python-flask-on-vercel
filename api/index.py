# old
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
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
        response = call_chatgpt_api(event.message.text)
        reply_msg = extract_reply_from_response(response)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

def call_chatgpt_api(message):
    import os
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")
    system_prompt = "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people!Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.\nUser: "  # Define your system prompt here
    prompt = system_prompt + message

    # Truncate messages to fit within the token limit
    max_tokens = 4097 - len(prompt)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message[:max_tokens]},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=100,
    )
    return response




def extract_reply_from_response(response):
    choices = response['choices']
    if len(choices) > 0:
        reply = choices[0]['message']['content']
        return reply.strip()
    else:
        return ""



if __name__ == "__main__":
    app.run()
