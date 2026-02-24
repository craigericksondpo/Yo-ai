# agents/workflow_builder/workflow_builder.py

from core.platform_agent import PlatformAgent
from core.envelope import AgentContext

class WorkflowBuilderAgent(PlatformAgent):
    """
    The Workflow Builder is a platform agent responsible for:
    - building complex workflows
    """

    def __init__(self, card, extended_card=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
        )

    # ------------------------------------------------------------------
    # Capability: Workflow.Build
    # ------------------------------------------------------------------
    async def workflow_build(self, envelope):
        from .workflow_build import run
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
