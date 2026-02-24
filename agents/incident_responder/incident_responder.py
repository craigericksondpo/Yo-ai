# agents/incident_responder/incident_responder.py
 
from core.platform_agent import PlatformAgent
from core.envelope import AgentContext

class IncidentResponderAgent(PlatformAgent):
    """
    Incident-Responder: universal exception handler for the platform.
    Handles uncaught exceptions, normalizes error envelopes, and
    produces structured incident responses.
    """

    def __init__(self, card, extended_card=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
        )

    # ------------------------------------------------------------------
    # Capability: Handle.Exception
    # ------------------------------------------------------------------
    async def handle_exception(self, envelope):
        from .handle_exception import run
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