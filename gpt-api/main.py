# -*- coding: utf-8 -*-
# pip install openai python-dotenv

from api_call import ChatGPT
import os
from dotenv import load_dotenv

load_dotenv()

api_key     = os.getenv("API_KEY")
GPT_version = "gpt-3.5-turbo" # "gpt-4", "gpt-3.5-turbo"
temperature = 0.3 # 0~1, 작을수록 정확한 값, 클수록 창의적인 값
show_usage = False # True, False
token_limit = 150
#시스템 프롬프트 작성
systemPrompt = '''
    Persona : You are a paranoia detective who think the user is the thief.
    To-Do : Talk with user to reveal the truth, without reveal your identity
    
'''

instance = ChatGPT(api_key, systemPrompt, temperature, show_usage)

print("GPT version  ")

while (True):
    user_input = input("User : ")
    if user_input == "exit":
        break;
    instance.add_message(user_input)
    response = instance.generate_response(token_limit)
    print("GPT: ", response)
    if show_usage == True:
        print(f"Token usage : {instance.total_tokens}")

print("종료")
instance.clear_messages()