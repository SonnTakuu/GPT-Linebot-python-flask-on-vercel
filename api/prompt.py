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

    def add_msg(self, new_msg):
        tokens = len(new_msg.split())
        if self.current_tokens + tokens > self.max_tokens:
            self.remove_excess_tokens(tokens)
        self.msg_list.append(new_msg)
        self.current_tokens += tokens

    def remove_excess_tokens(self, tokens):
        while self.current_tokens + tokens > self.max_tokens:
            removed_msg = self.msg_list.pop(0)
            self.current_tokens -= len(removed_msg.split())

    def generate_prompt(self):
        return '\n'.join(self.msg_list)



