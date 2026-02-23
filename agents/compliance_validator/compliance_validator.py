# agents/compliance_validator/compliance_validator.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class ComplianceValidatorAgent(YoAiAgent):
    """
    Compliance-Validator: evaluates facts, evidence, and assessments against
    laws, regulations, mandates, policies, and contracts. Produces factual
    compliance rationales suitable for audit, challenge, or testimony.

    This agent is profile-aware: compliance evaluation often depends on
    subject profile, caller identity, and governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Compliance-Standard.Get
    # ------------------------------------------------------------------
    async def compliance_standard_get(self, envelope):
        from .compliance_standard_get import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Compliance.Validate
    # ------------------------------------------------------------------
    async def compliance_validate(self, envelope):
        from .compliance_validate import run
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