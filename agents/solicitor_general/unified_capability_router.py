# agents/solicitor_general/unified_capability_router.py


from typing import Dict, Any, Callable, Optional

class UnifiedCapabilityRouter:
    def __init__(
        self,
        capability_map: Dict[str, str],
        handler_loader: Callable[[str], Callable],
        schema_validator: Callable[[str, Dict[str, Any]], bool],
        a2a_schema_index: Dict[str, str],
    ):
        """
        capability_map:
            messageType -> dotted import path for handler (semantic level)

        handler_loader:
            SG-provided function to import handler from dotted path

        schema_validator:
            SG-provided tool: validate(schema_id, instance) -> bool

        a2a_schema_index:
            A2A messageType -> schema_id (v0.3 or v1.0)
            Example:
                {
                    "SendMessage": "https://a2a/schemas/v1/send-message.schema.json",
                    "SendStreamingMessage": "...",
                    "TaskStatusUpdate": "...",
                }
        """
        self.capability_map = capability_map
        self.handler_loader = handler_loader
        self.schema_validator = schema_validator
        self.a2a_schema_index = a2a_schema_index

    # ----------------------------------------------------------------------
    # A2A-level discrimination
    # ----------------------------------------------------------------------

    def get_a2a_message_type(
        self,
        a2a_envelope: Dict[str, Any],
        governance_labels: Optional[list] = None,
    ) -> str:
        """
        Determine A2A messageType from JSON-RPC envelope.

        Strategy:
          1. Extract params.message top-level key (A2A v1.0 pattern).
          2. If ambiguous or missing, inspect governanceLabels for hints.
          3. Validate against known A2A schemas (v0.3 or v1.0).
          4. Return canonical A2A messageType.
        """
        params = a2a_envelope.get("params", {})
        message = params.get("message", {})

        # --- Step 1: direct extraction (A2A v1.0 pattern)
        if isinstance(message, dict) and len(message) == 1:
            candidate = next(iter(message.keys()))
            if candidate in self.a2a_schema_index:
                return candidate

        # --- Step 2: governanceLabels fallback
        if governance_labels:
            for item in governance_labels:
                if isinstance(item, dict) and "a2a_message_type" in item:
                    candidate = item["a2a_message_type"]
                    if candidate in self.a2a_schema_index:
                        return candidate

        # --- Step 3: schema-based discrimination (fallback)
        for msg_type, schema_id in self.a2a_schema_index.items():
            if self.schema_validator(schema_id, params):
                return msg_type

        raise ValueError("Unable to determine A2A messageType")

    # ----------------------------------------------------------------------
    # Semantic-level discrimination
    # ----------------------------------------------------------------------

    def get_semantic_message_type(self, envelope: Dict[str, Any]) -> str:
        """
        Extract semantic messageType from payload["message"].
        """
        payload = envelope.get("payload", {})
        message = payload.get("message", {})

        if not isinstance(message, dict) or len(message) != 1:
            raise ValueError("payload.message must contain exactly one top-level key")

        return next(iter(message.keys()))

    # ----------------------------------------------------------------------
    # Handler resolution (semantic level)
    # ----------------------------------------------------------------------

    def resolve_handler(self, message_type: str) -> Callable:
        """
        Resolve handler for semantic messageType.
        """
        dotted_path = self.capability_map.get(message_type)
        if not dotted_path:
            raise ValueError(f"No handler configured for messageType '{message_type}'")

        return self.handler_loader(dotted_path)

    # ----------------------------------------------------------------------
    # Main entry points
    # ----------------------------------------------------------------------

    def route_a2a(
        self,
        a2a_envelope: Dict[str, Any],
        governance_labels: Optional[list] = None,
    ) -> str:
        """
        Determine A2A messageType only.
        SG will handle everything else.
        """
        return self.get_a2a_message_type(a2a_envelope, governance_labels)

    def route_semantic(self, envelope: Dict[str, Any]) -> Callable:
        """
        Determine semantic messageType and return handler.
        SG will call the handler.
        """
        message_type = self.get_semantic_message_type(envelope)
        return self.resolve_handler(message_type)
