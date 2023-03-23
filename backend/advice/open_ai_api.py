import os

import openai

from backend.advice.advice_types import AdviceType
import backend.advice.prompt as prompt_gen
from backend.carbon.emissions import ResourceEmissionInfo

class OpenAIClient:
    """
    A Singleton class that represents an OpenAI client for generating advice based on resource emission information.
    """
    _instance = None

    def __init__(self):
        """
        Use thw key from the environment to initialize the OpenAI client.
        """
        openai.api_key = os.environ["OPEN_API_KEY"]
    
    # Implement OpenAIClient as a Singleton
    def __new__(cls):
        """
        Guarantees that only one instance of OpenAIClient is generated, according to the Singleton design principle.
        
        Returns:
            OpenAIClient: The unique instance of the OpenAIClient class.
        """
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
        return cls._instance
    
    def get_advice(self, resource_emission_infos: list[ResourceEmissionInfo], advice_type: AdviceType) -> str:
        """
        Generates advice based on the provided resource emission information and given specific advice type.

        Args:
            resource_emission_infos(list[ResourceEmissionInfo]): A list of ResourceEmissionInfo objects containing server information.
            advice_type (AdviceType): An of the AdviceType enum which indicates the type of advice to generate.

        Returns:
            str: The generated advice from OpenAI.
        """
        prompt = prompt_gen.get_prompt(resource_emission_infos, advice_type)
        print("prompt:", prompt, advice_type)
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=1,
        )
        print("response:", res)
        return res["choices"][0]["text"]
