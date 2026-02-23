# agents/purchasing_agent/purchasing_agent.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class PurchasingAgentAgent(YoAiAgent):
    """
    Purchasing-Agent: thin orchestration layer.
    Each capability method delegates to a capability-handler module.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Purchase-Options.Recommend
    # ------------------------------------------------------------------
    async def purchase_options_recommend(self, envelope):
        from .purchase_options_recommend import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Purchase-Risk.Evaluate
    # ------------------------------------------------------------------
    async def purchase_risk_evaluate(self, envelope):
        from .purchase_risk_evaluate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Purchase-History.Generate
    # ------------------------------------------------------------------
    async def purchase_history_generate(self, envelope):
        from .purchase_history_generate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Purchase-Receipt.Generate
    # ------------------------------------------------------------------
    async def purchase_receipt_generate(self, envelope):
        from .purchase_receipt_generate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Purchase-Issues.Resolve
    # ------------------------------------------------------------------
    async def purchase_issues_resolve(self, envelope):
        from .purchase_issues_resolve import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Return-Or-Refund.Initiate
    # ------------------------------------------------------------------
    async def return_or_refund_initiate(self, envelope):
        from .return_or_refund_initiate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Order-Status.Track
    # ------------------------------------------------------------------
    async def order_status_track(self, envelope):
        from .order_status_track import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Budget-After-Purchase.Update
    # ------------------------------------------------------------------
    async def budget_after_purchase_update(self, envelope):
        from .budget_after_purchase_update import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Transaction-Complete.Verify
    # ------------------------------------------------------------------
    async def transaction_complete_verify(self, envelope):
        from .transaction_complete_verify import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Purchase.Initiate
    # ------------------------------------------------------------------
    async def purchase_initiate(self, envelope):
        from .purchase_initiate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Purchase-Eligibility.Validate
    # ------------------------------------------------------------------
    async def purchase_eligibility_validate(self, envelope):
        from .purchase_eligibility_validate import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Budget.Check
    # ------------------------------------------------------------------
    async def budget_check(self, envelope):
        from .budget_check import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Payment.Cancel
    # ------------------------------------------------------------------
    async def payment_cancel(self, envelope):
        from .payment_cancel import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Mandate.Manage
    # ------------------------------------------------------------------
    async def mandate_manage(self, envelope):
        from .mandate_manage import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------
    def _build_context(self, envelope_dict):
        return AgentContext(
            caller=envelope_dict.get("caller"),
            subject=envelope_dict.get("subject"),
            profile=envelope_dict.get("profile"),
            profile_patch=envelope_dict.get("profilePatch"),
            governance_labels=envelope_dict.get("governanceLabels", []),
            correlation_id=envelope_dict.get("correlationId"),
        )
