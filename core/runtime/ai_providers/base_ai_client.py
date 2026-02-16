# core/runtime/ai_providers/base_ai_client.py

"""
BaseAIClient

Defines the canonical interface for all AI provider clients.
Every agent runtime uses an instance of a subclass of BaseAIClient.
"""

from abc import ABC, abstractmethod


class BaseAIClient(ABC):
    """
    Abstract base class for all AI provider clients.
    """

    def __init__(self, model: str, temperature: float = 0.2, max_tokens: int = 2048):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def chat_completion(self, system: str, user: str) -> str:
        """
        Execute a chat-style completion request.

        Parameters:
            system (str): system prompt
            user (str): user prompt (JSON string)

        Returns:
            str: raw model output (string)
        """
        raise NotImplementedError("chat_completion() must be implemented by subclasses")