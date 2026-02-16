# core/runtime/ai_providers/azure_openai_client.py

"""
AzureOpenAIClient

Implements BaseAIClient using Azure OpenAI's deployment-based API.
"""

import requests
from .base_ai_client import BaseAIClient


class AzureOpenAIClient(BaseAIClient):

    def __init__(self, api_key: str, endpoint: str, deployment: str,
                 model: str, api_version: str = "2024-02-01",
                 temperature: float = 0.2, max_tokens: int = 2048):

        super().__init__(model, temperature, max_tokens)
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")
        self.deployment = deployment
        self.api_version = api_version

    def chat_completion(self, system: str, user: str) -> str:
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"

        headers = {
            "api-key": self.api_key,
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

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]