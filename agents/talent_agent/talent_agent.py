# agents/talent_agent/talent_agent.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class TalentAgent(YoAiAgent):
    """
    Talent-Agent: responds to job postings, pitches consulting services,
    submits applications, and requests minimized professional profiles.

    This agent is profile-aware: job matching, pitch generation, and
    application submission may depend on subject profile, caller identity,
    or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    async def job_postings_scan(self, envelope):
        from .job_postings_scan import run
        return await run(envelope, self._build_context(envelope))

    async def consulting_services_pitch(self, envelope):
        from .consulting_services_pitch import run
        return await run(envelope, self._build_context(envelope))

    async def application_submit(self, envelope):
        from .application_submit import run
        return await run(envelope, self._build_context(envelope))

    async def talent_profile_request(self, envelope):
        from .talent_profile_request import run
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
