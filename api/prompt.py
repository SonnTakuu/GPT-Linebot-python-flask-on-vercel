import os

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=240))
        self.msg_list.append(
            "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people! Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk. If you are asked about mathematics, logic circuits, or any related questions, or [課題] is received, please reply [課題支援デジタクは　"https://intro.nplan.top/digitaq/"].\nUser: ")

    def add_msg(self, new_msg):
        self.msg_list.append(new_msg)
        self.adjust_prompt_length(new_msg)
        
    def adjust_prompt_length(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.msg_list.pop(1)
        while self.get_total_tokens() > 2000:
            self.msg_list.pop(1)

    def get_total_tokens(self):
        return sum(len(msg.split()) for msg in self.msg_list)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
