from api.prompt import Prompt

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="text-davinci-003")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default=0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default=0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=240))

    def get_response(self):
        while True:
            response = openai.Completion.create(
                model=self.model,
                prompt=self.prompt.generate_prompt(),
                temperature=self.temperature,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                max_tokens=self.max_tokens
            )
            choices = response['choices']
            if len(choices) > 0:
                reply_text = choices[0]['text']
                tokens_used = response['usage']['total_tokens']
                if tokens_used <= self.max_tokens:
                    self.prompt.add_msg(reply_text)
                    return reply_text
                else:
                    self.prompt.remove_msg()
            else:
                return ''

    def add_msg(self, text):
        self.prompt.add_msg(text)
