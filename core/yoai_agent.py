# core/yoai_agent.py

from core.agent import Agent
from core.runtime.load_fingerprints import load_fingerprints
from core.runtime.load_knowledge import load_knowledge
from importlib import import_module

from shared.tools.bootstrap_tools import build_tool_registry
from shared.tools.loaders.tool_invocation_manager import ToolInvocationManager


class YoAiAgent(Agent):
    """
    YoAiAgent:
    Identity-bearing, profile-aware, multi-instance agent.

    Responsibilities:
      - Load skills, schemas, and tools from card + extended card
      - Load runtime artifacts (fingerprints, knowledge)
      - Accept optional profile injection
      - Provide context-building helpers for capability execution

    No agent_id field — identity is derived from the AgentCard.
    """

    def __init__(self, *, card, extended_card=None, profile=None, context=None):
        super().__init__(card=card, extended_card=extended_card, context=context)

        # Optional profile injection
        self.profile = profile

        # Declarative contract loading
        self.skills = self._load_skills()
        self.schemas = self._load_schemas()

        # Manifest-driven tool loading
        registry = build_tool_registry(self.extended)
        self.tools = registry
        self.tool_manager = ToolInvocationManager(registry._adapters)

        # Runtime artifacts
        self.fingerprints = load_fingerprints(self.card, self.extended)
        self.knowledge = load_knowledge(self)

    # ------------------------------------------------------------------
    # Loader: Skills
    # ------------------------------------------------------------------
    def _load_skills(self):
        skills = list(self.card.get("skills", []))
        if self.extended:
            skills += self.extended.get("skills", [])
        return skills

    # ------------------------------------------------------------------
    # Loader: Schemas
    # ------------------------------------------------------------------
    def _load_schemas(self):
        schemas = list(self.card.get("schemas", []))
        if self.extended:
            schemas += self.extended.get("schemas", [])
        return schemas

    # ------------------------------------------------------------------
    # Error Handler: Universal safety net for direct agent invocation
    # ------------------------------------------------------------------
    def handle_capability(
        self,
        capability_name: str,
        payload: dict,
        request_id: any | None = None,
    ):
        """
        Safe capability entrypoint.

        If Solicitor-General is present, it will wrap this call.
        If Solicitor-General is absent (tests, scripts, notebooks), 
        this method ensures ANY exception becomes an AnyException 
        wrapped in a JSON-RPC envelope.
        """
        from core.runtime.error_handler import ErrorHandler

        # Capability lookup
        handler = getattr(self, capability_name, None)

        if handler is None or not callable(handler):
            # Known error path: capability does not exist
            return ErrorHandler.from_known_error(
                code=-32601,  # JSON-RPC "Method not found"
                message="Capability not found",
                request_id=request_id,
                extra={
                    "agent": self.card.get("name"),
                    "capability": capability_name,
                    "source": "YoAiAgent.handle_capability",
                },
            )

        try:
            # Normal capability execution path
            return handler(payload)

        except Exception as exc:
            # Universal normalization path (SG absent)
            return ErrorHandler.normalize_exception(
                exc,
                request_id=request_id,
                agent_name=self.card.get("name"),
                capability=capability_name,
                context={
                    "source": "YoAiAgent.handle_capability",
                },
            )