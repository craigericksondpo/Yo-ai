# agents/data_steward/data_steward.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class DataSteward(YoAiAgent):
    """
    Data-Steward: governs access to personal data, evaluates intended use,
    and acts on behalf of a specific person.

    This agent is profile-aware: it must be constructed with a profileRef
    or loaded profile context.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Phone.Call
    # ------------------------------------------------------------------
    async def phone_call(self, envelope):
        from .phone_call import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Phone.Answer
    # ------------------------------------------------------------------
    async def phone_answer(self, envelope):
        from .phone_answer import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Data-Request.Govern
    # ------------------------------------------------------------------
    async def data_request_govern(self, envelope):
        from .data_request_govern import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Email.Read
    # ------------------------------------------------------------------
    async def email_read(self, envelope):
        from .email_read import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Email.Send
    # ------------------------------------------------------------------
    async def email_send(self, envelope):
        from .email_send import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------
    def _build_context(self, envelope_dict):
        """
        Build AgentContext using:
          - caller
          - subject
          - profile (from constructor or envelope)
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
