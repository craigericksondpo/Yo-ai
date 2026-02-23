# agents/profile_builder/profile_builder.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class ProfileBuilderAgent(YoAiAgent):
    """
    Profile-Builder: builds and maintains organization profiles based on
    discovery from IP-Inspector and Tech-Inspector agents.

    This agent is profile-aware: it may operate with an org profile reference
    or build a new one from scratch.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Org-Profile.Build
    # ------------------------------------------------------------------
    async def org_profile_build(self, envelope):
        from .org_profile_build import run
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
