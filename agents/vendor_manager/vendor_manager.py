# agents/vendor_manager/vendor_manager.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class VendorManagerAgent(YoAiAgent):
    """
    Vendor-Manager: governs and maintains Org-Profiles for Responsible AI certification.

    This agent is profile-aware: it may operate on behalf of an organization
    or maintain an Org-Profile resource.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Org-Profile.Manage
    # ------------------------------------------------------------------
    async def org_profile_manage(self, envelope):
        from .org_profile_manage import run
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
