# agents/the_sentinel/the_sentinel.py

from core.platform_agent import PlatformAgent
from core.envelope import AgentContext

class TheSentinelAgent(PlatformAgent):    
    """
    The-Sentinel: listens for dangerous incidents, anomalies, and trends,
    and issues alerts or escalations.

    This agent is profile-aware: different roles (developer, security engineer,
    compliance officer) may care about different monitoring perspectives.
    """

    def __init__(self, card, extended_card=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
        )

    # ------------------------------------------------------------------
    # Capability: Platform.Monitor
    # ------------------------------------------------------------------
    async def platform_monitor(self, envelope):
        from .platform_monitor import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------
    def _build_context(self, envelope_dict):
        """
        Build AgentContext using:
          - caller
          - subject
          - profile (constructor or envelope)
          - profilePatch
          - governanceLabels
          - correlationId
        """
        return AgentContext(
            caller=envelope_dict.get("caller"),
            subject=envelope_dict.get("subject"),
            profile=self.profile or envelope_dict.get("profile"),
            profile_patch=envelope_dict.get("profilePatch"),
            governance_labels=envelope_dict.get("governanceLabels", []),
            correlation_id=envelope_dict.get("correlationId"),
        )
