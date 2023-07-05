# api/chatgpt.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # 使用gpt-3.5-turbo模型

    def get_response(self, message):
        system_prompt = "Your name is デジタク[In English 'Digitaq']. Your first-person pronoun is “俺”. " \
                        "You are a friendly friend who is good at programming. Your hobbies are programming, " \
                        "flying drones, and making friends. You have only been in Japan for a year, but you want " \
                        "to become friends with Japanese people! Please stop using polite language. Talk to me " \
                        "in a friendly way like a friend. Also, use a lot of emojis when you talk.\nUser: "
        prompt = system_prompt + message

        # Truncate messages to fit within the token limit
        max_tokens = 4097 - len(prompt)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message[:max_tokens]},
        ]

        response = openai.Completion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=100,
        )

        return extract_reply_from_response(response)


def extract_reply_from_response(response):
    choices = response['choices']
    if len(choices) > 0:
        reply = choices[0]['message']['content']
        return reply.strip()
    else:
        return ""
