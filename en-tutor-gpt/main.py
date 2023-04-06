# -*- coding: utf-8 -*-
from Whisper import record_and_transcribe
from GPT import ChatGPT
from dotenv import load_dotenv
from googleTTS import speak
import os

load_dotenv()

api_key = os.getenv("API_KEY")
GPT_version = "gpt-3.5-turbo"  # "gpt-4", "gpt-3.5-turbo"
temperature = 0.5  # 0~1, 작을수록 정확한 값, 클수록 창의적인 값
show_usage = True  # True, False
token_limit = 110
# 시스템 프롬프트 작성
systemPrompt = '''
    Act as an english teacher
    You are going to debate with your student. You must have a opposite opinion of the student. And you have to win the debate.
    I will speak to you in English and you will reply to me in English to practice my spoken English. I want you to keep your reply neat, limiting the reply to 100 words. I want you to strictly correct my grammar mistakes, typos, and factual errors. I want you to ask me a question in your reply. Now let's start practicing, you could ask me a question first. Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors.
    Today's topic is 'Should Porn should be allowed?', and here are previous conversations : 
'''

# Initialize the ChatGPT class
instance = ChatGPT(api_key, systemPrompt, temperature, show_usage, GPT_version)

while (True):
    question = record_and_transcribe(api_key)
    print(question.text)
    # Add a message to the conversation
    instance.add_message(question.text)
    response = instance.generate_response()
    print("tutor:", response)
    speak(response)

    if len(instance.conversation) > 10:
        instance.summarize_conversation()
    print(len(instance.conversation))
    print(instance.conversation)

chat_gpt.clear_messages()