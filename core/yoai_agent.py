# core/yoai_agent.py

import uuid
from core.base_agent import BaseAgent
from core.runtime.logger import logger
from core.runtime.load_fingerprints import load_fingerprints
from core.runtime.load_knowledge import load_knowledge
from core.runtime.logging.log_bootstrapper import get_logger
from importlib import import_module

from shared.tools.bootstrap_tools import build_tool_registry
from shared.tools.loaders.tool_invocation_manager import ToolInvocationManager


class YoAiAgent(BaseAgent):
    """
    YoAiAgent:
    Identity-bearing, profile-aware, multi-instance agent.

    Responsibilities:
      - Load skills, schemas, and tools from card + extended card
      - Load runtime artifacts (fingerprints, knowledge)
      - Accept optional profile injection
      - Provide context-building helpers for capability execution
    """

    def __init__(self, *, card, extended_card=None, profile=None, context=None):
        super().__init__(card=card, extended_card=extended_card, context=context)


        # Agent identity
        self.actor_name - self.card.get("name", "unknown-agent") 
                
        # Optional profile injection
        self.profile = profile

        # Correlation context (set per message/task)
        self.correlation_id = None

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

        # Platform-wide logging
        self.logger = get_logger(self.actor_name)
        self.logger.write( 
            {"actor": self.actor_name,
             "event_type": "agent_initialized",
             "message": f"{self.actor_name} initialized",
             "payload": {}
             }
        )


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
    # Correlation context management
    # ------------------------------------------------------------------
    def set_correlation(self, correlation_id: str = None):
        """
        Sets the active correlation ID for this agent.
        Called automatically by messgae/task handlers.
        """
        self.correlation_id = correlation_id or str(uuid.uuid4())

    def clear_correlation(self):
        """
        Clears the correlation context after a message/task completes.
        """
        self.correlation_id = None

    # ------------------------------------------------------------------
    # Logging wrapper with automatic correlation injection
    # ------------------------------------------------------------------
    def log(self, event_type: str, message: str, payload: dict = None, level: str = "INFO"):
        """
        Writes a structured log event with automatic correlation ID.
        """
        self.logger.write(
            {
            "actor": self.actor_name,
            "event_type": event_type,
            "message": message,
            "payload": payload or {},
            "correlation_id": self.correlation_id
            }
        )

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