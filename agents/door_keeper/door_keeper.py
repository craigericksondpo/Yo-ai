# agents/door_keeper/door_keeper.py

from core.platform_agent import PlatformAgent
from core.envelope import AgentContext

class DoorKeeperAgent(PlatformAgent):
    """
    Door-Keeper: profiles guests, registers subscribers/agents,
    authenticates visitors, assigns trust, and manages access rights.

    This agent is profile-aware: it may operate with a subject profile
    or visitor profile depending on the envelope.
    """

    def __init__(self, card, extended_card=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
        )

    # ------------------------------------------------------------------
    # Capability: Visitor.Identify
    # ------------------------------------------------------------------
    async def visitor_identify(self, envelope):
        from .visitor_identify import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Subscriber.Register
    # ------------------------------------------------------------------
    async def subscriber_register(self, envelope):
        from .subscriber_register import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Credentials.Generate
    # ------------------------------------------------------------------
    async def credentials_generate(self, envelope):
        from .credentials_generate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Subscriber.Authenticate
    # ------------------------------------------------------------------
    async def subscriber_authenticate(self, envelope):
        from .subscriber_authenticate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Agent.Register
    # ------------------------------------------------------------------
    async def agent_register(self, envelope):
        from .agent_register import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Trust.Assign
    # ------------------------------------------------------------------
    async def trust_assign(self, envelope):
        from .trust_assign import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: AccessRights.Manage
    # ------------------------------------------------------------------
    async def accessrights_manage(self, envelope):
        from .accessrights_manage import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Agent.Authenticate
    # ------------------------------------------------------------------
    async def agent_authenticate(self, envelope):
        from .agent_authenticate import run
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
