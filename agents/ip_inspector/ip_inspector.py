# agents/ip_inspector/ip_inspector.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class IPInspector(YoAiAgent):
    """
    IP-Inspector: discovers intellectual property, maps IP to products,
    searches for implementation instances, infers use cases, clusters portfolios,
    generates reports, evaluates risk, traces provenance, and discovers related IP.

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
    async def ip_assets_discover(self, envelope):
        from .ip_assets_discover import run
        return await run(envelope, self._build_context(envelope))

    async def ip_to_products_map(self, envelope):
        from .ip_to_products_map import run
        return await run(envelope, self._build_context(envelope))

    async def implementation_instances_search(self, envelope):
        from .implementation_instances_search import run
        return await run(envelope, self._build_context(envelope))

    async def use_cases_infer(self, envelope):
        from .use_cases_infer import run
        return await run(envelope, self._build_context(envelope))

    async def ip_portfolio_cluster(self, envelope):
        from .ip_portfolio_cluster import run
        return await run(envelope, self._build_context(envelope))

    async def ip_report_generate(self, envelope):
        from .ip_report_generate import run
        return await run(envelope, self._build_context(envelope))

    async def ip_risk_evaluate(self, envelope):
        from .ip_risk_evaluate import run
        return await run(envelope, self._build_context(envelope))

    async def ip_provenance_trace(self, envelope):
        from .ip_provenance_trace import run
        return await run(envelope, self._build_context(envelope))

    async def related_ip_discover(self, envelope):
        from .related_ip_discover import run
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
