# chatgpt.py
from api.prompt import Prompt

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = "gpt-3.5-turbo"  # 使用gpt-3.5-turbo模型
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0.8))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=2048))

    def get_response(self):
        response = openai.Completion.create(
            model=self.model,
            prompt=self.prompt.generate_prompt(),
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            max_tokens=self.max_tokens
        )
        return response['choices'][0]['text'].strip()

    def add_msg(self, text):
        self.prompt.add_msg(text)


# prompt.py
import os

MSG_LIST_LIMIT = 10  # 最大保存10回合对话


class Prompt:
    def __init__(self):
        self.msg_list = []
        self.msg_list.append(
            "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. "
            "You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, "
            "and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people! "
            "Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk."
        )

    def add_msg(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.remove_msg()
        self.msg_list.append(new_msg)

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
