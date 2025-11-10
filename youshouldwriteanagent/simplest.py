# Simplest LLM conv loop
# Inspired by https://fly.io/blog/everyone-write-an-agent/

from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()
context = []

def call_llm():
    return client.responses.create(model='gpt-5-mini', input=context)

def process_user_input(line):
    context.append({'role': 'user', 'content': line})
    response = call_llm()
    context.append({'role': 'assistant', 'content': response.output_text})
    return response.output_text

def main():
    while True:
        user_input = input("> ")
        llm_result_from_user_input = process_user_input(user_input)
        print(f">>> {llm_result_from_user_input}\n")

if __name__ == "__main__":
    main()



