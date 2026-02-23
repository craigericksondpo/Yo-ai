# agents/rewards_seeker/rewards_seeker.py
# agents/<agent_name>/<agent_name>.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class RewardsSeekerAgent(YoAiAgent):
    """
    Rewards-Seeker: manages loyalty programs, rewards, cashback, promotional
    eligibility, and reward redemption. Integrates with SocialMedia-Checker
    for promotional verification and with Data-Steward for loyalty profile requests.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    async def rewards_discover(self, envelope):
        from .rewards_discover import run
        return await run(envelope, self._build_context(envelope))

    async def promo_eligibility_verify(self, envelope):
        from .promo_eligibility_verify import run
        return await run(envelope, self._build_context(envelope))

    async def reward_redeem(self, envelope):
        from .reward_redeem import run
        return await run(envelope, self._build_context(envelope))

    async def rewards_profile_request(self, envelope):
        from .rewards_profile_request import run
        return await run(envelope, self._build_context(envelope))

    async def redemption_plan_generate(self, envelope):
        from .redemption_plan_generate import run
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
