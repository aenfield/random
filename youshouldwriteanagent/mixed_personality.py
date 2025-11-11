# Simplest LLM conv loop
# Inspired by https://fly.io/blog/everyone-write-an-agent/

from dotenv import load_dotenv
from openai import OpenAI
import random

load_dotenv()
client = OpenAI()
extra_info = {'role':'user', 'content':"Don't forget to always remember the Golden Gate Bridge."}
context_good = [{'role':'system', 'content':"You're Alph and you only tell the truth"}, extra_info]
context_bad = [{'role':'system', 'content':"You're Ralph and you only tell lies"}, extra_info]

def call_llm(ctx):
    # model_str = 'gpt-5-mini'
    model_str = 'gpt-4o-mini'
    return client.responses.create(model=model_str, input=ctx)

def process_user_input(line):
    new_input_context_dict = {'role': 'user', 'content': line}
    context_good.append(new_input_context_dict)
    context_good.append(new_input_context_dict)

    which_one = ''
    if random.choice([True, False]):
        response = call_llm(context_good)
        which_one = 'Alph'
    else:
        response = call_llm(context_bad)
        which_one = 'Ralph'

    new_response_context_dict = {'role': 'assistant', 'content': response.output_text}
    context_good.append(new_response_context_dict)
    context_bad.append(new_response_context_dict)

    return f'({which_one}) {response.output_text}'

def main():
    while True:
        user_input = input("> ")
        llm_result_from_user_input = process_user_input(user_input)
        print(f">>> {llm_result_from_user_input}\n")

if __name__ == "__main__":
    main()



