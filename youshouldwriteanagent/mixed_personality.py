# Simplest LLM conv loop
# Inspired by https://fly.io/blog/everyone-write-an-agent/

from dotenv import load_dotenv
from openai import OpenAI
import random

client = OpenAI()
context_good = [{'role':'system', 'content':"You're Alph and you only tell the truth"}]
context_bad = [{'role':'system', 'content':"You're Ralph and you only tell lies"}]

def call_llm(ctx):
    return client.responses.create(model='gpt-5-mini', input=ctx)

def process_user_input(line):
    new_input_context_dict = {'role': 'user', 'content': line}
    context_good.append(new_input_context_dict)
    context_good.append(new_input_context_dict)

    if random.choice([True, False]):
        response = call_llm(context_good)
    else:
        response = call_llm(context_bad)

    new_response_context_dict = {'role': 'assistant', 'content': response.output_text}
    context_good.append(new_response_context_dict)
    context_bad.append(new_response_context_dict)

    return response.output_text

def main():
    while True:
        user_input = input("> ")
        llm_result_from_user_input = process_user_input(user_input)
        print(f">>> {llm_result_from_user_input}\n")

if __name__ == "__main__":
    main()



