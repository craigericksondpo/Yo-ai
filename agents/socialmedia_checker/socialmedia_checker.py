# agents/socialmedia_checker/socialmedia_checker.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class SocialMediaCheckerAgent(YoAiAgent):
    """
    SocialMedia-Checker: evaluates social media activity to verify promotional
    requirements and detect potential misappropriation of personal data.

    This agent is profile-aware: verification and misappropriation detection
    may depend on subject profile, caller identity, or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    async def promotional_engagement_verify(self, envelope):
        from .promotional_engagement_verify import run
        return await run(envelope, self._build_context(envelope))

    async def misappropriation_detect(self, envelope):
        from .misappropriation_detect import run
        return await run(envelope, self._build_context(envelope))

    async def evidence_collect(self, envelope):
        from .evidence_collect import run
        return await run(envelope, self._build_context(envelope))

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
