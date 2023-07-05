import openai
import os

from prompt import Prompt

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
