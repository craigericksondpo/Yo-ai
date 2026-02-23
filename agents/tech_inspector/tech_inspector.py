# agents/tech_inspector/tech_inspector.py

from core.yoai_agent import YoAiAgent
from core.envelope import AgentContext


class TechInspectorAgent(YoAiAgent):
    """
    Tech-Inspector: discovers third-party assets, maps integrations, analyzes
    implementation details, searches usage instances, infers technical impact,
    clusters portfolios, evaluates integration risk, traces provenance, detects
    related assets, and generates technical reports.

    This agent is profile-aware: analysis may depend on subject profile,
    caller identity, or governance labels.
    """

    def __init__(self, card, extended_card=None, profile=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=profile,
        )

    # ------------------------------------------------------------------
    async def third_party_assets_discover(self, envelope):
        from .third_party_assets_discover import run
        return await run(envelope, self._build_context(envelope))

    async def asset_integrations_map(self, envelope):
        from .asset_integrations_map import run
        return await run(envelope, self._build_context(envelope))

    async def implementation_details_analyze(self, envelope):
        from .implementation_details_analyze import run
        return await run(envelope, self._build_context(envelope))

    async def usage_instances_search(self, envelope):
        from .usage_instances_search import run
        return await run(envelope, self._build_context(envelope))

    async def technical_impact_infer(self, envelope):
        from .technical_impact_infer import run
        return await run(envelope, self._build_context(envelope))

    async def asset_portfolio_cluster(self, envelope):
        from .asset_portfolio_cluster import run
        return await run(envelope, self._build_context(envelope))

    async def integration_risk_evaluate(self, envelope):
        from .integration_risk_evaluate import run
        return await run(envelope, self._build_context(envelope))

    async def integration_provenance_trace(self, envelope):
        from .integration_provenance_trace import run
        return await run(envelope, self._build_context(envelope))

    async def related_assets_detect(self, envelope):
        from .related_assets_detect import run
        return await run(envelope, self._build_context(envelope))

    async def tech_report_generate(self, envelope):
        from .tech_report_generate import run
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
