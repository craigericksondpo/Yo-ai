# core/runtime/ai_providers/claude_client.py

"""
ClaudeClient

Implements BaseAIClient using Anthropic's Claude API (Sonnet, Opus, Haiku).
"""

import requests
from .base_ai_client import BaseAIClient


class ClaudeClient(BaseAIClient):

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-sonnet-20240229",
        endpoint: str = "https://api.anthropic.com/v1/messages",
        temperature: float = 0.2,
        max_tokens: int = 2048
    ):
        super().__init__(model, temperature, max_tokens)
        self.api_key = api_key
        self.endpoint = endpoint

    def chat_completion(self, system: str, user: str) -> str:
        """
        Executes a Claude message completion request.

        Anthropic uses a "system" field + a list of messages.
        """

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "system": system,
            "messages": [
                {"role": "user", "content": user}
            ]
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        # Claude returns content as a list of blocks
        if "content" in data and isinstance(data["content"], list):
            # Extract only text blocks
            text_blocks = [
                block.get("text", "")
                for block in data["content"]
                if block.get("type") == "text"
            ]
            return "\n".join(text_blocks)

        # Fallback: return raw JSON
        return str(data)