import openai

class ChatGPT:
    def __init__(self, api_key, systemPrompt, temp, showUsage):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = api_key
        self.conversation = [
                   {"role": "system", "content": systemPrompt},
        ]
        self.temperature = temp
        self.toggleUsage = showUsage
        self.total_tokens = 0
    def add_message(self, message, role="user"):
        self.conversation.append({"role": role, "content": message})

    def clear_messages(self):
        self.messages = []

    def generate_response(self, max_tokens=150):
        response = self.openai.ChatCompletion.create(
            model="gpt-4",
            messages = self.conversation,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=self.temperature,
        )

        response_text = response.choices[0].message.content

        #사용량 체크
        if self.toggleUsage == True:
            used_tokens = response.usage.total_tokens
            self.total_tokens += used_tokens

        self.add_message(response_text, role="assistant")
        return response_text