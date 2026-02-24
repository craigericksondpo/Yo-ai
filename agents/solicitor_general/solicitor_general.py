# agents/solicitor_general/solicitor_general.py

from core.platform_agent import PlatformAgent
from core.envelope import AgentContext


class SolicitorGeneralAgent(PlatformAgent):
    """
    Solicitor-General:
    Root governance agent for the Yo-AI Platform.

    Responsibilities:
      - Broker all A2A interactions
      - Enforce call-graph rules and trust tiers
      - Maintain correlation maps and routing continuity
      - Manage task lifecycle and dispatch
      - Log events and maintain platform auditability

    PlatformAgents do NOT use profiles — they do not represent people.
    """

    def __init__(self, *, card, extended_card=None, context=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            context=context,
        )

    async def just_ask(self, envelope):
        from .just_ask import run
        return await run(envelope, self._build_context(envelope))

    async def event_log(self, envelope):
        from .event_log import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Context builder (PlatformAgents do NOT use profiles)
    # ------------------------------------------------------------------
    def _build_context(self, envelope_dict):
        return AgentContext(
            caller=envelope_dict.get("caller"),
            subject=envelope_dict.get("subject"),
            profile=None,  
            profile_patch=None,
            governance_labels=envelope_dict.get("governanceLabels", []),
            correlation_id=envelope_dict.get("correlationId"),
        )
