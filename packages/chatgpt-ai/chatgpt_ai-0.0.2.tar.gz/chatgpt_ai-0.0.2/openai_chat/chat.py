import openai
import json

class Chat:
    message_history: list[dict[str, str]] = []

    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                self.message_history = json.load(f)

    def send(self, message=None, role='user') -> dict:
        if not message and not self.message_history:
            print("Must provide a message to start a chat")
            return {}
        if message:
            self.message_history.append({
                'role': role,
                'content': message,
            })

        res = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.3,
            max_tokens=100,
            messages=self.message_history,
        )
        response = res['choices'][0]['message']

        self.message_history.append(response)
        return response

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.message_history, f, indent=2)

    def display_message(self, message: dict):
        self.display_sep(message['role'])
        print(message['content'] + "\n")

    def display_sep(self, role: str):
        if role == 'system':
            c = "*"
        elif role == 'user':
            c = "="
        else:
            c = '-'
        print(c * 50)

    def display_history(self):
        for message in self.message_history:
            self.display_message(message)

