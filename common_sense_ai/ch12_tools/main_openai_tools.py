# this is the main.py code, updated to replace the bespoke home-grown tool calling
# impl with the impl required by OpenAI's API

from dotenv import load_dotenv
from openai import OpenAI
import json
import re
import requests
from bs4 import BeautifulSoup

load_dotenv()
llm = OpenAI()

def llm_response(prompt, tools_spec):
    response = llm.responses.create(
        model = 'gpt-5-mini',
        tools = tools_spec,
        input = prompt
    )
    return response

# def extract_function(response):
#     # detect the home-grown function notation we tell the LLM to use:
#     # <<function(arg1, arg2)>>
#     pattern = r'<<\s*([a-zA-Z_]\w*)\s*\(([^)]+)\)\s*>>'
#     match = re.search(pattern, response)

#     if not match:
#         # no function requested by the LLM, so we're done
#         return None
    
#     function_name = match.group(1)
#     function_args = match.group(2).split(',')

#     # now see if we have a requested function and return it if so
#     if function_name == 'multiply':
#         return multiply(*function_args) 
#     elif function_name == 'read_webpage':
#         return read_webpage(*function_args)
#     else:
#         return None
    
def multiply(first_num, second_num):
    return float(first_num) * float(second_num)

def read_webpage(url):
    print(f'Trying to retrieve {url}...')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text

TOOLS_SPEC = [
    {
        'type': 'function',
        'name': 'multiply',
        'description': 'Multiply two numbers to generate a product.',
        'parameters': {
            'type': 'object',
            'properties': {
                'first_num': {'type': 'integer'},
                'second_num': {'type': 'integer'},
            },
            'required': ['first_num', 'second_num']
        }
    },
    {
        'type': 'function',
        'name': 'read_webpage',
        'description': 'Accesses a web page and obtains its text.',
        'parameters': {
            'type': 'object',
            'properties': {
                'url': {
                    'type': 'string',
                    'description': 'The URL of the web page'
                }
            },
            'required': ['url']
        }
    }
]

def main_loop():
    print('\nAssistant: How can I help today?\n')
    user_input = input('User: ')
    history = [
        {'role': 'developer', 'content': """You are a helpful AI assistant. If you ever need to 
        multiply two numbers, DO NOT attempt to answer with your internal knowledge. 
        Instead, use your multiply tool."""},
        {'role': 'assistant', 'content': 'How can I help today?'}
    ]

    while user_input != 'exit':
        if user_input == 'history':
            print(history)
            # print(json.dumps(history, indent=2), '\n')
        else:
            history += [{'role': 'user', 'content': user_input}]
            response = llm_response(history, TOOLS_SPEC)

            history += response.output # store the whole response object, not just the text, so we can pass back function call details in subsequent calls

            for item in response.output:
                if item.type == 'function_call':
                    function_call = item
                    function_name = item.name
                    function_args = json.loads(item.arguments)

                    if function_name == 'multiply':
                        result = {'multiply': multiply(**function_args)}
                    elif function_name == 'read_webpage':
                        result = {'read_webpage': read_webpage(**function_args)}

                    history += [{
                        'type': 'function_call_output',
                        'call_id': function_call.call_id,
                        'output': json.dumps(result)
                    }]

                    # and call the LLM again to interpret/incorporate the tool result
                    response = llm_response(history, TOOLS_SPEC)
            
            history += [{'role': 'assistant', 'content': response.output_text}]

            print(f'\nAssistant: {response.output_text}\n')

        user_input = input('User: ')

if __name__ == '__main__':
    main_loop()
