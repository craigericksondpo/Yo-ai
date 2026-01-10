# 4. Worker agents as PI-blind consumers
# From the worker side, they interact with Data Steward, not with the vault.
# purchasing-agent.py placeholder (pseudo Python)

class RewardsSeeker:
    def __init__(self, data_steward: DataSteward):
        self.data_steward = data_steward

    async def evaluate_offer(self, offer: Dict[str, Any]) -> Dict[str, Any]:
        context: OpportunityContext = {
            "opportunity_id": offer["offer_id"],
            "source_agent_id": "rewards-seeker",
            "category": "rewards",
            "vendor_id": offer.get("vendor_id"),
            "description": offer.get("description"),
            "tags": offer.get("tags", []),
            "metadata": {"raw_offer": offer},
        }

        profile_bundle = await self.data_steward.prepare_rewards_profile(context)

        # Work only with minimized profile_bundle.fields
        # No direct vault access here
        decision = self._score_offer(offer, profile_bundle.fields)

        return {
            "offer_id": offer["offer_id"],
            "decision": decision,
            "used_fields": list(profile_bundle.fields.keys()),
        }
# Purchasing Agent and Talent Agent follow the same pattern: they’re consumers of minimized bundles.

