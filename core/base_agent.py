# core/base_agent.py

from __future__ import annotations
from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class Agent(Protocol):
    """
    A2A v1.0 structural agent interface.

    This Protocol defines the *shape* of an A2A-compliant agent.
    It does NOT define transport, schema validation, or runtime behavior.

    Any object with:
      - name: str
      - capabilities: list[str]
      - handle_request(request) -> dict

    …is considered an Agent, regardless of inheritance.
    """

    name: str
    capabilities: list[str]

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        Process a well-formed A2A v1.0 request and return an A2A v1.0 response.
        """
        ...


class BaseAgent:
    """
    BaseAgent:
    Concrete helper class for YoAiAgent and PlatformAgent.

    Responsibilities:
      - Store card + extended card
      - Provide identity fields (name, capabilities)
      - Provide a safe handle_request() wrapper
      - Provide JSON-RPC error normalization
      - Provide a capability lookup helper

    This class is NOT the A2A interface — the Protocol above is.
    This class is the shared runtime behavior for platform-native agents.
    """

    def __init__(self, *, card: dict, extended_card: dict | None = None, context: dict | None = None):
        self.card = card or {}
        self.extended = extended_card or {}
        self.context = context or {}

        # Identity is card-driven
        self.name = self.card.get("name", "unknown-agent")

        # Capabilities declared in the card(s)
        caps = list(self.card.get("capabilities", []))
        if self.extended:
            caps += self.extended.get("capabilities", [])
        self.capabilities = caps

    # ------------------------------------------------------------------
    # Core A2A entrypoint
    # ------------------------------------------------------------------
    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        Default A2A request handler.

        YoAiAgent and PlatformAgent override this to implement:
          - caller identity extraction
          - capability negotiation
          - artifact selection
          - logging and governance
          - routing to capability handlers

        This method provides a universal safety net:
          - JSON-RPC envelope normalization
          - AnyException wrapping
        """
        from core.runtime.error_handler import ErrorHandler

        request_id = request.get("id")
        method = request.get("method")

        # Capability lookup
        handler = getattr(self, method, None)

        if handler is None or not callable(handler):
            return ErrorHandler.from_known_error(
                code=-32601,
                message="Capability not found",
                request_id=request_id,
                extra={
                    "agent": self.name,
                    "capability": method,
                    "source": "BaseAgent.handle_request",
                },
            )

        try:
            params = request.get("params", {})
            return handler(params)

        except Exception as exc:
            return ErrorHandler.normalize_exception(
                exc,
                request_id=request_id,
                agent_name=self.name,
                capability=method,
                context={"source": "BaseAgent.handle_request"},
            )

    # ------------------------------------------------------------------
    # Optional helper for subclasses
    # ------------------------------------------------------------------
    def get_capability(self, name: str):
        """
        Retrieve a capability handler by name.
        Subclasses may use this for routing.
        """
        return getattr(self, name, None)