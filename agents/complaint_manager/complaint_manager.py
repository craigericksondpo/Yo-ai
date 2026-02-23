# agents/complaint_manager/complaint_manager.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext

class ComplaintManagerAgent(YoAiAgent):
    """
    Complaint-Manager is a YoAiAgent representing a person or org rep.
    It loads skills/tools/schemas/fingerprints/knowledge from YoAiAgent.
    """

    def __init__(self, agent_id="complaint_manager", profile=None,
                 card=None, extended_card=None, context=None):

        super().__init__(card=card, extended_card=extended_card, context=context)

        self.agent_id = agent_id
        self.profile = profile  # profileRef or loaded profile

    # ------------------------------------------------------------------
    # Capability: Liability.Discover
    # ------------------------------------------------------------------
    async def liability_discover(self, envelope):
        from .liability_discover import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: EnforcementAgency.Get
    # ------------------------------------------------------------------
    async def enforcementagency_get(self, envelope):
        from .enforcementagency_get import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Stakeholders.Get
    # ------------------------------------------------------------------
    async def stakeholders_get(self, envelope):
        from .stakeholders_get import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Complaint.Generate
    # ------------------------------------------------------------------
    async def complaint_generate(self, envelope):
        from .complaint_generate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Complaint.Submit
    # ------------------------------------------------------------------
    async def complaint_submit(self, envelope):
        from .complaint_submit import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Complaint.Publish
    # ------------------------------------------------------------------
    async def complaint_publish(self, envelope):
        from .complaint_publish import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Stakeholder.Notify
    # ------------------------------------------------------------------
    async def stakeholder_notify(self, envelope):
        from .stakeholder_notify import run
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