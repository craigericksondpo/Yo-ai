# core/runtime/ai_providers/provider_orchestrator.py

"""
ProviderOrchestrator

Coordinates multiple AI providers for a single agent.

Responsibilities:
- Load provider configs from agent x-ai block
- Select a provider based on strategy (failover, round-robin)
- Cache provider health in-memory (per process / Lambda container)
- Retry with alternate providers on failure
"""

import logging
import time
from typing import Any, Dict, List, Optional

from .provider_loader import load_ai_provider

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ProviderOrchestrator:
    """
    Orchestrates multiple AI providers for an agent.

    Expected config structure (from agent card x-ai):

    {
        "providers": [
            {
                "provider": "anthropic",
                "model": "claude-3-sonnet-20240229",
                "api_key_env": "ANTHROPIC_API_KEY"
            },
            {
                "provider": "openai",
                "model": "gpt-4.2",
                "api_key_env": "OPENAI_API_KEY"
            }
        ],
        "strategy": "failover" | "round-robin",
        "health_ttl_seconds": 300
    }
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config or {}
        self.providers_config: List[Dict[str, Any]] = self.config.get("providers", [])
        self.strategy: str = self.config.get("strategy", "failover")
        self.health_ttl_seconds: int = self.config.get("health_ttl_seconds", 300)

        if not self.providers_config:
            raise ValueError("ProviderOrchestrator requires at least one provider in x-ai.providers")

        # In-memory health + round-robin state (per process / Lambda container)
        self._health_cache: Dict[int, Dict[str, Any]] = {}
        self._rr_index: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def chat_completion(self, system: str, user: str) -> str:
        """
        Execute a chat completion using the configured strategy and providers.
        """

        if self.strategy == "round-robin":
            return self._chat_completion_round_robin(system, user)

        # Default: failover
        return self._chat_completion_failover(system, user)

    # ------------------------------------------------------------------
    # Strategy: Failover
    # ------------------------------------------------------------------
    def _chat_completion_failover(self, system: str, user: str) -> str:
        last_error: Optional[Exception] = None

        for idx, provider_cfg in enumerate(self.providers_config):
            if not self._is_provider_healthy(idx):
                logger.info(f"[ProviderOrchestrator] Skipping unhealthy provider index={idx}")
                continue

            try:
                client = load_ai_provider(provider_cfg)
                logger.info(f"[ProviderOrchestrator] Using provider index={idx} cfg={provider_cfg}")
                result = client.chat_completion(system, user)
                self._mark_provider_healthy(idx)
                return result

            except Exception as e:
                logger.warning(f"[ProviderOrchestrator] Provider index={idx} failed: {e}")
                self._mark_provider_unhealthy(idx)
                last_error = e
                continue

        # If we exhausted all providers
        if last_error:
            raise RuntimeError(f"All AI providers failed. Last error: {last_error}") from last_error

        raise RuntimeError("No available AI providers")

    # ------------------------------------------------------------------
    # Strategy: Round-robin (with health awareness)
    # ------------------------------------------------------------------
    def _chat_completion_round_robin(self, system: str, user: str) -> str:
        attempts = 0
        total = len(self.providers_config)
        last_error: Optional[Exception] = None

        while attempts < total:
            idx = self._rr_index % total
            self._rr_index += 1
            attempts += 1

            if not self._is_provider_healthy(idx):
                logger.info(f"[ProviderOrchestrator] Skipping unhealthy provider index={idx}")
                continue

            provider_cfg = self.providers_config[idx]

            try:
                client = load_ai_provider(provider_cfg)
                logger.info(f"[ProviderOrchestrator] (RR) Using provider index={idx} cfg={provider_cfg}")
                result = client.chat_completion(system, user)
                self._mark_provider_healthy(idx)
                return result

            except Exception as e:
                logger.warning(f"[ProviderOrchestrator] (RR) Provider index={idx} failed: {e}")
                self._mark_provider_unhealthy(idx)
                last_error = e
                continue

        if last_error:
            raise RuntimeError(f"All AI providers failed (round-robin). Last error: {last_error}") from last_error

        raise RuntimeError("No available AI providers (round-robin)")

    # ------------------------------------------------------------------
    # Health tracking
    # ------------------------------------------------------------------
    def _is_provider_healthy(self, idx: int) -> bool:
        """
        Returns True if provider is considered healthy or health has expired.
        """
        entry = self._health_cache.get(idx)
        if not entry:
            return True  # no history → assume healthy

        if entry.get("healthy", True):
            return True

        # If unhealthy, check TTL
        ts = entry.get("timestamp", 0)
        if (time.time() - ts) > self.health_ttl_seconds:
            logger.info(f"[ProviderOrchestrator] Health TTL expired for provider index={idx}, re-enabling")
            return True

        return False

    def _mark_provider_unhealthy(self, idx: int):
        self._health_cache[idx] = {
            "healthy": False,
            "timestamp": time.time()
        }

    def _mark_provider_healthy(self, idx: int):
        self._health_cache[idx] = {
            "healthy": True,
            "timestamp": time.time()
        }