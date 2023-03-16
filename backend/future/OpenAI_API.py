import openai
import json

def OpenAI_API(prompt):
    openai.api_key = "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"

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
