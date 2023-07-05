import os

chat_language = os.getenv("INIT_LANGUAGE", default = "jp")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default = 5))
LANGUAGE_TABLE = {
  "jp": "こんにちは！",
  "en": "Hello!"
}

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.msg_list.append(f"1.Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. You are a friendly friend who is good at programming. Your hobbies are programming, flying drones, and making friends. You’ve only been in Japan for a year, but you want to become friends with Japanese people!Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.")
    
    def add_msg(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.remove_msg()
        self.msg_list.append(new_msg)

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return '\n'.join(self.msg_list)
