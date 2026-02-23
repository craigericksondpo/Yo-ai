# agents/risk_assessor/risk_assessor.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class RiskAssessorAgent(YoAiAgent):
    """
    Risk-Assessor: conducts structured, provenance-aware risk assessments using
    specified standards, evidence sources, and assessment models.

    This agent is profile-aware: assessments may depend on subject profile,
    caller identity, org-profile, or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Risks.Assess
    # ------------------------------------------------------------------
    async def risks_assess(self, envelope):
        from .risks_assess import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------
    def _build_context(self, envelope_dict):
        return AgentContext(
            caller=envelope_dict.get("caller"),
            subject=envelope_dict.get("subject"),
            profile=self.profile or envelope_dict.get("profile"),
            profile_patch=envelope_dict.get("profilePatch"),
            governance_labels=envelope_dict.get("governanceLabels", []),
            correlation_id=envelope_dict.get("correlationId"),
        )
