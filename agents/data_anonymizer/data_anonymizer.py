# agents/data_anonymizer/data_anonymizer.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class DataAnonymizer(YoAiAgent):
    """
    Data-Anonymizer: uses a variety of tools and techniques for anonymizing
    and testing datasets of personal attributes.

    This agent is profile-aware: anonymization decisions may depend on
    subject profile, caller identity, or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    async def identifiability_assess(self, envelope):
        from .identifiability_assess import run
        return await run(envelope, self._build_context(envelope))

    async def deidentification_techniques_apply(self, envelope):
        from .deidentification_techniques_apply import run
        return await run(envelope, self._build_context(envelope))

    async def k_anonymity_compute(self, envelope):
        from .k_anonymity_compute import run
        return await run(envelope, self._build_context(envelope))

    async def safe_release_recommend(self, envelope):
        from .safe_release_recommend import run
        return await run(envelope, self._build_context(envelope))

    async def deidentification_report_generate(self, envelope):
        from .deidentification_report_generate import run
        return await run(envelope, self._build_context(envelope))

    async def auxiliary_data_risk_evaluate(self, envelope):
        from .auxiliary_data_risk_evaluate import run
        return await run(envelope, self._build_context(envelope))

    async def data_for_purpose_minimize(self, envelope):
        from .data_for_purpose_minimize import run
        return await run(envelope, self._build_context(envelope))

    async def reidentification_attack_simulate(self, envelope):
        from .reidentification_attack_simulate import run
        return await run(envelope, self._build_context(envelope))

    async def deidentification_standard_map(self, envelope):
        from .deidentification_standard_map import run
        return await run(envelope, self._build_context(envelope))

    async def deidentification_guidance_publish(self, envelope):
        from .deidentification_guidance_publish import run
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
