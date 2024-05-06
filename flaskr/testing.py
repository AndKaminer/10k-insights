import os

import openai


with open(os.path.join(os.getcwd(), ".env"), "r") as key:
    k = key.readline().rstrip('\n')
    client = openai.OpenAI(api_key=k)

completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #{"role": "system", "content": "You are a helpful assistant who is an expert in reading financial statements. You will be provided with two financial statements. Please compare and contrast them."},
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of Wisconsin?"}
            ])

print(completion.choices[0].message.content)
