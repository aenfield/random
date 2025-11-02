from dotenv import load_dotenv
from openai import OpenAI
import json
import re

load_dotenv()
llm = OpenAI()

def llm_response(prompt):
    response = llm.responses.create(
        model = 'gpt-4.1-nano',
        temperature = 0,
        input = prompt
    )
    return response

def extract_function(response):
    # detect the home-grown function notation we tell the LLM to use:
    # <<function(arg1, arg2)>>
    pattern = r'<<\s*([a-zA-Z_]\w*)\s*\(([^)]+)\)\s*>>'
    match = re.search(pattern, response)

    if not match:
        # no function requested by the LLM, so we're done
        return None
    
    function_name = match.group(1)
    function_args = match.group(2).split(',')

    # now see if we have a requested function and return it if so
    if function_name == 'multiply':
        return multiply(*function_args) 
    # elif function__name == 'read_webpage':
    #     return read_webpage(*function_args)
    else:
        return None
    
def multiply(first_num, second_num):
    return float(first_num) * float(second_num)

def main_loop():
    print('\nAssistant: How can I help today?\n')
    user_input = input('User: ')
    history = [
        {'role': 'developer', 'content': """You are a helpful AI assistant. If you ever need to 
        multiply two numbers, DO NOT attempt to answer with your internal knowledge. 
        Instead, output a special notation with double angle brackets like this: <<multiply(first_number, second_number)>>.
        For example, if a user asks you to multiply 50 by 2, your output should be: <<multiply(50, 2)}>>. A second example:
        a user asks you how many apples there are in five baskets and each basket contains twelve apples. Your output
        should be: <<multiply(5, 12)>>.
        If you are ever provided info contained within <info> tags, use that
        info in your response to the user. Using an answer inside <info> tags takes precedence over all
        other instructions."""},
        {'role': 'assistant', 'content': 'How can I help today?'}
    ]

    while user_input != 'exit':
        if user_input == 'history':
            print(json.dumps(history, indent=2), '\n')
        else:
            history += [{'role': 'user', 'content': user_input}]
            response = llm_response(history)

            # check to see if the LLM response has a request to call a function
            function_result = extract_function(response.output_text)
            if function_result:
                # there was one, so run it and then give the output of the function
                # to the LLM, so the LLM can decide what to do with it (including if
                # and how to display it) - i.e., we don't automatically print just
                # the function's output
                history += [{'role': 'user', 'content': f"""Here is information to use to respond to
                             the user's previous query: <info>{function_result}</info>"""}]  
                # print(json.dumps(history, indent=2))
                response = llm_response(history)

            history += [{'role': 'assistant', 'content': response.output_text}]

            print(f'\nAssistant: {response.output_text}\n')

        user_input = input('User: ')

if __name__ == '__main__':
    main_loop()
