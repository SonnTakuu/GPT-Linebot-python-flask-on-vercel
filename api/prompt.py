import os

chat_language = os.getenv("INIT_LANGUAGE", default="zh")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}


class Prompt:
    def __init__(self):
        self.msg_list = []
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=240))
        self.msg_list.append(
            "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people! Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.\nUser: ")

    def add_msg(self, new_msg):
        self.msg_list.append(new_msg)
        self.adjust_prompt_length(new_msg)
        
    def adjust_prompt_length(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.msg_list.pop(0)
        while self.get_total_tokens() > 4096:
            self.msg_list.pop(0)

    def get_total_tokens(self):
        return sum(len(msg.split()) for msg in self.msg_list)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
