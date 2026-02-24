# agents/decision_master/decision_master.py

from core.platform_agent import PlatformAgent
from core.envelope import AgentContext

class DecisionMasterAgent(PlatformAgent):
    """
    Decision-Master: identifies and analyzes decision-making events,
    manages decision diaries, and publishes decision outcomes.

    This agent is profile-aware: decision analysis may depend on
    subject profile, caller identity, or governance labels.
    """

    def __init__(self, card, extended_card=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
        )

    # ------------------------------------------------------------------
    # Capability: Decision-Diary.Manage
    # ------------------------------------------------------------------
    async def decision_diary_manage(self, envelope):
        from .decision_diary_manage import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Decision-Events.Identify
    # ------------------------------------------------------------------
    async def decision_events_identify(self, envelope):
        from .decision_events_identify import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Decision-Outcome.Identify
    # ------------------------------------------------------------------
    async def decision_outcome_identify(self, envelope):
        from .decision_outcome_identify import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Decision-Outcome.Analyze
    # ------------------------------------------------------------------
    async def decision_outcome_analyze(self, envelope):
        from .decision_outcome_analyze import run
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
