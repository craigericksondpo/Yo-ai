# core/runtime/ai_providers/openai_client.py

"""
OpenAIClient

Implements BaseAIClient using the OpenAI-compatible API.
"""

import requests
from .base_ai_client import BaseAIClient


class OpenAIClient(BaseAIClient):

    def __init__(self, api_key: str, model: str, endpoint: str = "https://api.openai.com/v1/chat/completions",
                 temperature: float = 0.2, max_tokens: int = 2048):
        super().__init__(model, temperature, max_tokens)
        self.api_key = api_key
        self.endpoint = endpoint

    def chat_completion(self, system: str, user: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]