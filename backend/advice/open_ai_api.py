import os

import openai

def get_advice(prompt):
    openai.api_key = os.environ["OPEN_API_KEY"]

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text = response["choices"][0]["text"]
    
    return text
