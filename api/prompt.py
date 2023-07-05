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
        self.current_tokens = 0
        self.msg_list.append(
            "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You have only been in Japan for a year, but you want to become friends with Japanese people! Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.\nUser: ")

    def add_msg(self, new_msg):
        tokens = len(new_msg.split())
        while self.current_tokens + tokens > self.max_tokens:
            removed_msg = self.msg_list.pop(0)
            self.current_tokens -= len(removed_msg.split())
        self.msg_list.append(new_msg)
        self.current_tokens += tokens


    def adjust_messages(self, tokens_to_remove):
        while tokens_to_remove > 0:
            removed_msg = self.msg_list.pop(0)
            tokens_removed = len(removed_msg.split())
            tokens_to_remove -= tokens_removed

    def get_total_tokens(self):
        return sum(len(msg.split()) for msg in self.msg_list)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
