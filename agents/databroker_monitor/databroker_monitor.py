# agents/databroker_monitor/databroker_monitor.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class DataBrokerMonitor(YoAiAgent):
    """
    DataBroker-Monitor: monitors registered data brokers to detect possession,
    sale, or distribution of personal information and identify downstream purchasers.

    This agent is profile-aware: investigations may depend on subject profile,
    caller identity, or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    # Capability: Broker-Inventory.Scan
    # ------------------------------------------------------------------
    async def broker_inventory_scan(self, envelope):
        from .broker_inventory_scan import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Downstream-Vendors.Identify
    # ------------------------------------------------------------------
    async def downstream_vendors_identify(self, envelope):
        from .downstream_vendors_identify import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Capability: Broker-Evidence.Collect
    # ------------------------------------------------------------------
    async def broker_evidence_collect(self, envelope):
        from .broker_evidence_collect import run
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
