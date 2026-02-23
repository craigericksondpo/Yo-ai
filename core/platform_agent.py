# core/platform_agent.py

from core.yoai_agent import YoAiAgent


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
        event = {
            "type": change_type,
            "details": details or {},
            "source": self.card.get("name"),
        }

        # Platform runtime handles fan-out to all PlatformAgents
        await self.runtime.broadcast_platform_event(
            "Platform.ConfigurationChanged",
            event
        )
