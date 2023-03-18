import os

import openai

from backend.advice.advice_types import AdviceType
import backend.advice.prompt as prompt
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
    
    def get_advice(self, resource_emission_infos: list[ResourceEmissionInfo], advice_type: AdviceType) -> str:
        return openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt.get_prompt(resource_emission_infos, advice_type),
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )["choices"][0]["text"]
