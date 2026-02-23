# agents/darkweb_checker/darkweb_checker.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class DarkWebChecker(YoAiAgent):
    """
    DarkWeb-Checker: searches breach forums, marketplaces, and dark web sources
    for stolen PI — and collects evidence to support claims that an organization
    acquired or used stolen data.

    This agent is profile-aware: investigations may depend on subject profile,
    caller identity, or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Dark-Web.Scan
    # ------------------------------------------------------------------
    async def dark_web_scan(self, envelope):
        from .dark_web_scan import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Data-Origins.Trace
    # ------------------------------------------------------------------
    async def data_origins_trace(self, envelope):
        from .data_origins_trace import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Dark-Web-Evidence.Collect
    # ------------------------------------------------------------------
    async def dark_web_evidence_collect(self, envelope):
        from .dark_web_evidence_collect import run
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
