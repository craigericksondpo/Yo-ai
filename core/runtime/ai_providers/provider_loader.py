# core/runtime/ai_providers/provider_loader.py

"""
Provider Loader

Creates an AI provider client based on agent configuration.
This is the factory that turns agent card config → AI client instance.
"""

import os

from .openai_client import OpenAIClient
from .azure_openai_client import AzureOpenAIClient
from .claude_client import ClaudeClient


def load_ai_provider(config: dict):
    """
    Load an AI provider client based on the agent's configuration.

    Expected config structure (from agent card or runtime):
    {
        "provider": "openai" | "azure-openai" | "anthropic",
        "model": "gpt-4.2" | "gpt-4o" | "claude-3-sonnet-20240229",
        "temperature": 0.2,
        "max_tokens": 2048,
        "endpoint": "...",        # optional
        "deployment": "...",      # Azure only
        "api_key_env": "OPENAI_API_KEY" | "AZURE_OPENAI_KEY" | "ANTHROPIC_API_KEY"
    }
    """

    provider = config.get("provider")
    model = config.get("model")
    temperature = config.get("temperature", 0.2)
    max_tokens = config.get("max_tokens", 2048)
    api_key_env = config.get("api_key_env")

    if not provider:
        raise ValueError("AI provider not specified in agent configuration")

    if not model:
        raise ValueError("AI model not specified in agent configuration")

    if not api_key_env:
        raise ValueError("api_key_env must be provided to load AI provider")

    api_key = os.getenv(api_key_env)
    if not api_key:
        raise RuntimeError(f"Environment variable {api_key_env} is not set")

    # ------------------------------------------------------------
    # OpenAI (direct API)
    # ------------------------------------------------------------
    if provider == "openai":
        endpoint = config.get("endpoint", "https://api.openai.com/v1/chat/completions")
        return OpenAIClient(
            api_key=api_key,
            model=model,
            endpoint=endpoint,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ------------------------------------------------------------
    # Azure OpenAI (deployment-based)
    # ------------------------------------------------------------
    if provider == "azure-openai":
        endpoint = config.get("endpoint")
        deployment = config.get("deployment")

        if not endpoint or not deployment:
            raise ValueError("Azure OpenAI requires 'endpoint' and 'deployment'")

        return AzureOpenAIClient(
            api_key=api_key,
            endpoint=endpoint,
            deployment=deployment,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ------------------------------------------------------------
    # Anthropic Claude (Sonnet, Opus, Haiku)
    # ------------------------------------------------------------
    if provider == "anthropic":
        endpoint = config.get("endpoint", "https://api.anthropic.com/v1/messages")
        return ClaudeClient(
            api_key=api_key,
            model=model,
            endpoint=endpoint,
            temperature=temperature,
            max_tokens=max_tokens
        )

    # ------------------------------------------------------------
    # Unknown provider
    # ------------------------------------------------------------
    raise ValueError(f"Unknown AI provider: {provider}")