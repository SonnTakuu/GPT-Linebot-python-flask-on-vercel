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
        self.msg_list.append(
            "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people! Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.\nUser: ")

    def add_msg(self, new_msg):
        self.msg_list.append(new_msg)
        self.check_token_limit()

    def check_token_limit(self):
        total_tokens = sum(len(msg.split()) for msg in self.msg_list)
        if total_tokens > int(os.environ.get("OPENAI_MAX_TOKENS", 240)):
            self.remove_msg()

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
