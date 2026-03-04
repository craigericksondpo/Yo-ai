# core/platform_agent.py

import json
from pathlib import Path
from typing import Dict, Any, Optional

from core.yoai_agent import YoAiAgent
from core.runtime import logger


class PlatformAgent(YoAiAgent):
    """
    PlatformAgent:
    Privileged, long-lived, platform-service agent.

    Responsibilities:
      - Inherit all loading behavior from YoAiAgent (skills, tools, schemas,
        fingerprints, knowledge)
      - Enforce platform-level constraints (call graph, trust tiers, etc.)
      - Expose platform services to YoAiAgents and Visiting Agents
      - Maintain singleton-like lifecycle (managed by the platform)
      - Receive and optionally react to platform configuration changes (CM-6)
      - Emit configuration change events when modifying platform behavior

    PlatformAgents do NOT use profiles — they do not represent people.
    """

    def __init__(self, *, card, extended_card=None, context=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=None,      # PlatformAgents never use profiles
            context=context,
        )

    # ------------------------------------------------------------------
    # CM-6: Receive configuration change notifications
    # ------------------------------------------------------------------
    async def on_platform_configuration_change(self, event):
        """
        Called when the platform detects a significant configuration change.
        PlatformAgents may override this to react, but they are not required to.
        """
        self.log.info(f"[CM-6] Configuration change received: {event.get('type')}")

    # ------------------------------------------------------------------
    # CM-6: Emit configuration change events
    # ------------------------------------------------------------------
    async def emit_configuration_changed(self, change_type, details=None):
        """
        Emit a Platform.ConfigurationChanged event to notify all PlatformAgents.
        Required for NIST 800-53 CM-6 compliance.
        """
        self.log.info(
            f"[CM-6] Configuration changed: {change_type}",
            extra={
                "event_type": "platform_configuration_changed",
                "change_type": change_type,
                "details": details or {},
                "source": self.name,
            }
        )

    async def authorize_call(self, envelope: Dict[str, Any]) -> bool:
        """
        Check if a specific A2A call is authorized.
        
        Args:
            envelope: A2A call envelope with caller info
            
        Returns:
            bool: True if authorized, False if denied
        """
        from runtime.authorize_call import run
        
        context = self._build_context(envelope)
        return await run(envelope, context)