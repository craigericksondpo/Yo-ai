# agents/solicitor_general/solicitor_general.py

from datetime import datetime
from .unified_capability_router import UnifiedCapabilityRouter
from core.platform_agent import PlatformAgent


class SolicitorGeneralAgent(PlatformAgent):
    """
    Solicitor-General:
    Root governance agent for the Yo-AI Platform.

    Responsibilities:
      - Interpret semantic capabilities from envelopes
      - Resolve capabilities to agents via capability_map
      - Instantiate agents via constructors
      - Maintain correlation lineage
      - Delegate dispatch to UnifiedCapabilityRouter

    PlatformAgents do NOT use profiles — they do not represent people.
    """

    def __init__(self, *, card, extended_card=None, context=None,
                 capability_map: dict | None = None,
                 constructors: dict | None = None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            context=context,
        )

        self.capability_map = capability_map or {}
        self.constructors = constructors or {}

        self.router = UnifiedCapabilityRouter(logger=self.logger)

    # ------------------------------------------------------------------
    # SG entrypoint (called by A2ATransport)
    # ------------------------------------------------------------------
    async def route(self, envelope: dict, request_id: str) -> dict:
        """
        SG requires request_id. Transport layer guarantees it is present.
        SG performs semantic routing based on capability_map.
        """

        self.logger.info("sg.received", extra={
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "envelope": envelope,
        })

        try:
            capability_name, payload = self._extract_capability(envelope)
            agent_name, agent_instance, handler_name = self._resolve_agent_for_capability(
                capability_name
            )
            agent_context = self._build_agent_context(
                envelope=envelope,
                request_id=request_id,
                agent_name=agent_name,
                agent_instance=agent_instance,
                capability_name=capability_name,
                payload=payload
            )
        except Exception as e:
            self.logger.error("sg.semantic_resolution_error", extra={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
                "error": str(e),
            })
            return {
                "error": {
                    "type": "SemanticResolutionError",
                    "message": str(e),
                }
            }

        try:
            result = await self.router.route(
                envelope=envelope,
                request_id=request_id,
                agent_context=agent_context,
                capability_name=capability_name,
                handler_name=handler_name,
                payload=payload
            )
        except Exception as e:
            self.logger.error("sg.routing_error", extra={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
                "agent_name": agent_name,
                "capability_name": capability_name,
                "error": str(e),
            })
            return {
                "error": {
                    "type": "RoutingError",
                    "message": str(e),
                }
            }

        self.logger.info("sg.completed", extra={
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "agent_name": agent_name,
            "capability_name": capability_name,
            "result": result,
        })

        return result

    # ------------------------------------------------------------------
    # Permissive capability extraction (v0.3, v1.0, future)
    # ------------------------------------------------------------------
    def _extract_capability(self, envelope: dict) -> tuple[str, dict]:
        """
        Permissive capability extraction supporting:
          - A2A v0.3  (params = payload directly, method = capability)
          - A2A v1.0  (params.message = { capability: payload })
          - Future versions (ignore unknown fields)

        No normalization is performed. SG treats all versions identically
        except for fields that exist.
        """

        params = envelope.get("params", {})

        # --- v1.0 shape: params.message = { capability: payload }
        if isinstance(params, dict) and "message" in params:
            message_container = params.get("message", {})
            if isinstance(message_container, dict) and len(message_container) == 1:
                capability_name = next(iter(message_container.keys()))
                payload = message_container[capability_name]
                return capability_name, payload
            # If malformed, fall through to permissive fallback

        # --- v0.3 shape: method = capability, params = payload
        method = envelope.get("method")
        if isinstance(method, str) and isinstance(params, dict):
            return method, params

        # --- Future versions: fallback error
        raise ValueError("Unable to extract capability from envelope")

    # ------------------------------------------------------------------
    # Capability → Agent resolution via capability_map
    # ------------------------------------------------------------------
    def _resolve_agent_for_capability(self, capability_name: str):
        capabilities = self.capability_map.get("capabilities", {})
        constructors = self.capability_map.get("constructors", {})

        if capability_name not in capabilities:
            raise ValueError(f"Unknown capability: {capability_name}")

        entry = capabilities[capability_name]

        agent_name = entry.get("agent")
        handler_name = entry.get("handler")

        if not agent_name:
            raise ValueError(f"Capability '{capability_name}' missing 'agent' in capability_map")

        if not handler_name:
            raise ValueError(f"Capability '{capability_name}' missing 'handler' in capability_map")

        constructor_name = agent_name
        constructor = constructors.get(constructor_name)

        if constructor is None:
            raise ValueError(
                f"No constructor found for agent '{agent_name}' "
                f"(expected key '{constructor_name}' in capability_map.constructors)"
            )

        agent_instance = constructor()

        return agent_name, agent_instance, handler_name

    # ------------------------------------------------------------------
    # Context builder (PlatformAgents do NOT use profiles)
    # ------------------------------------------------------------------
    def _build_agent_context(
        self,
        envelope: dict,
        request_id: str,
        agent_name: str,
        agent_instance,
        capability_name: str,
        payload: dict
    ):
        params = envelope.get("params", {})

        task_id = payload.get("task_id", request_id)

        return AgentContext(
            agent_name=agent_name,
            agent_instance=agent_instance,
            capability_name=capability_name,
            caller=params.get("caller"),
            subject=params.get("subject"),
            profile=None,
            profile_patch=None,
            governance_labels=params.get("governanceLabels", []),
            correlation_id=request_id,
            task_id=task_id
        )
