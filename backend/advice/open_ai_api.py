import os
import functools

import openai

from backend.advice.advice_types import AdviceType
import backend.advice.prompt as prompt_gen
from backend.carbon.emissions import ResourceEmissionInfo

class OpenAIClient:

    _instance = None

    def __init__(self):
        openai.api_key = os.environ["OPEN_API_KEY"]
    
    # Implement OpenAIClient as a Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
        return cls._instance
    
    @functools.cache
    def get_advice(self, resource_emission_infos: list[ResourceEmissionInfo], advice_type: AdviceType) -> str:
        prompt = prompt_gen.get_prompt(resource_emission_infos, advice_type)
        print("prompt", prompt, advice_type)
        return openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=512,
            temperature=0.5,
        )["choices"][0]["text"]
