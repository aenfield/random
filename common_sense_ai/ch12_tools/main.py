from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
llm = OpenAI()

def llm_response(prompt):
    response = llm.responses.create(
        model = 'gpt-4.1-nano',
        temperature = 0,
        input = prompt
    )
    return response

def main_loop():
    print('\nAssistant: How can I help today?\n')
    user_input = input('User: ')
    history = [
        {'role': 'developer', 'content': 'You are a helpful AI assistant.'},
        {'role': 'assistant', 'content': 'How can I help today?'}
    ]

    while user_input != 'exit':
        if user_input == 'history':
            print(json.dumps(history, indent=2), '\n')
        else:
            history += [{'role': 'user', 'content': user_input}]
            response = llm_response(history)
            print(f'\nAssistant: {response.output_text}\n')
            history += [
                {'role': 'assistant', 'content': response.output_text}
            ]

        user_input = input('User: ')

if __name__ == '__main__':
    main_loop()
