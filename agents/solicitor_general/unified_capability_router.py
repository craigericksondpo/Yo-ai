# /agents/solicitor_general/unified_capability_router.py

class UnifiedCapabilityRouter:
    """
    Semantic router for A2A messages.
    Owned by the Solicitor-General and called as its internal tool.

    Responsibilities:
    - Extract params.message
    - Detect messageType
    - (Hook) Validate payload schema
    - Resolve target agent (delegated to SG via AgentContext)
    - Hydrate agent
    - Invoke capability handler
    """

    def __init__(self, logger):
        self._logger = logger

    async def route(self, envelope: dict, request_id: str, agent_context) -> dict:
        params = envelope.get("params", {})
        message_container = params.get("message", {})

        # 1. Detect A2A messageType
        if not isinstance(message_container, dict) or len(message_container) != 1:
            raise ValueError("Invalid A2A message: expected exactly one messageType")

        message_type = next(iter(message_container.keys()))
        payload = message_container[message_type]

        # 2. Schema validation hook
        self._validate_message(message_type, payload)

        # 3. Resolve target agent via AgentContext (SG will supply this)
        agent = agent_context.resolve_agent()

        # 4. Resolve capability handler
        if not hasattr(agent, message_type):
            raise ValueError(
                f"Agent '{agent_context.agent_name}' does not implement capability '{message_type}'"
            )

        handler = getattr(agent, message_type)

        # 5. Execute capability handler
        try:
            result = await handler(payload)
        except Exception as e:
            self._logger.error("router.handler_error", extra={
                "request_id": request_id,
                "message_type": message_type,
                "agent_name": agent_context.agent_name,
                "error": str(e),
            })
            raise

        # 6. Return semantic result
        return result

    def _validate_message(self, message_type: str, payload: dict):
        """
        Schema validation hook.
        Replace with your actual schema library integration when ready.
        """
        return
