# unified_capability_router.py

import importlib
import logging
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


class CapabilityResolutionError(Exception):
    pass


class UnifiedCapabilityRouter:
    """
    Platform-wide semantic router for the Yo-AI platform.

    Two-level discrimination
    ------------------------
    A2A protocol level  — what wire format / JSON-RPC messageType is this?
                          Handled by route_a2a() and get_a2a_message_type().
    Semantic level      — what capability does this trigger, and who handles it?
                          Handled by route_semantic() and get_semantic_message_type().

    The full path from raw A2A envelope to invoked handler is covered by route(),
    which chains both levels automatically.

    Dependencies (injected, not owned)
    -----------------------------------
    handler_loader    : callable(dotted_path: str) -> Callable
                        Provided by the Solicitor-General. Used at dispatch time
                        for any handler not pre-loaded from YAML.
    schema_validator  : callable(schema_id: str, instance: dict) -> bool
                        Provided by the Solicitor-General. Used for schema-based
                        messageType discrimination when direct extraction fails.
    a2a_schema_index  : dict[messageType -> schema_id]
                        Maps known A2A messageTypes to their schema identifiers.

    YAML loading
    ------------
    Use the from_yaml() factory at startup to pre-load all handlers via importlib.
    This resolves dotted import paths eagerly so failures are loud and early.

        router = UnifiedCapabilityRouter.from_yaml(
            "capability_map.yaml",
            handler_loader=sg.load_handler,
            schema_validator=sg.validate_schema,
            a2a_schema_index=A2A_SCHEMA_INDEX,
        )

    Programmatic registration is also supported for tests:

        router = UnifiedCapabilityRouter(...)
        router.register_capability("Profile.Patch", my_handler)
    """

    def __init__(
        self,
        handler_loader: Callable[[str], Callable],
        schema_validator: Callable[[str, Dict[str, Any]], bool],
        a2a_schema_index: Dict[str, str],
    ) -> None:
        self.handler_loader    = handler_loader
        self.schema_validator  = schema_validator
        self.a2a_schema_index  = a2a_schema_index

        self.capability_map:     Dict[str, Callable] = {}
        self.message_type_map:   Dict[str, Callable] = {}
        self.agent_constructors: Dict[str, Callable] = {}

    # ------------------------------------------------------------------
    # Factory — build from YAML
    # ------------------------------------------------------------------

    @classmethod
    def from_yaml(
        cls,
        yaml_path: str | os.PathLike,
        handler_loader: Callable[[str], Callable],
        schema_validator: Callable[[str, Dict[str, Any]], bool],
        a2a_schema_index: Dict[str, str],
    ) -> "UnifiedCapabilityRouter":
        """
        Load capability_map.yaml and eagerly resolve all handlers via importlib.

        All handler values in the YAML must be dotted import paths, e.g.:
            agents.data_steward.capabilities.profile.profile_patch_handler

        Raises
        ------
        FileNotFoundError         - yaml_path does not exist
        CapabilityResolutionError - a handler string cannot be imported
        """
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(
                f"capability_map.yaml not found: {path.resolve()}"
            )

        with path.open() as f:
            config = yaml.safe_load(f) or {}

        router = cls(
            handler_loader=handler_loader,
            schema_validator=schema_validator,
            a2a_schema_index=a2a_schema_index,
        )

        for cap_name, entry in (config.get("capabilities") or {}).items():
            handler_str = entry["handler"] if isinstance(entry, dict) else entry
            handler = cls._import(handler_str, context=cap_name)
            router.register_capability(cap_name, handler)
            logger.debug("Registered capability    %s -> %s", cap_name, handler_str)

        for mt_name, handler_str in (config.get("messageTypes") or {}).items():
            handler = cls._import(handler_str, context=mt_name)
            router.register_message_type(mt_name, handler)
            logger.debug("Registered messageType   %s -> %s", mt_name, handler_str)

        for agent_name, constructor_str in (config.get("constructors") or {}).items():
            constructor = cls._import(constructor_str, context=agent_name)
            router.register_agent_constructor(agent_name, constructor)
            logger.debug("Registered constructor   %s -> %s", agent_name, constructor_str)

        logger.info(
            "UnifiedCapabilityRouter loaded from %s  "
            "(%d capabilities, %d messageTypes, %d constructors)",
            path,
            len(router.capability_map),
            len(router.message_type_map),
            len(router.agent_constructors),
        )
        return router

    # ------------------------------------------------------------------
    # Registration APIs  (programmatic / test use)
    # ------------------------------------------------------------------

    def register_capability(self, capability: str, handler: Callable) -> None:
        self.capability_map[capability] = handler

    def register_message_type(self, message_type: str, handler: Callable) -> None:
        self.message_type_map[message_type] = handler

    def register_agent_constructor(self, agent_name: str, constructor: Callable) -> None:
        self.agent_constructors[agent_name] = constructor

    # ------------------------------------------------------------------
    # Main entry point - full pipeline
    # ------------------------------------------------------------------

    async def route(
        self,
        a2a_envelope: Dict[str, Any],
        governance_labels: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        Full pipeline: raw A2A envelope -> invoked handler -> result.

        Steps
        -----
        1. Determine A2A messageType from the wire envelope.
        2. Extract the semantic messageType from the unwrapped payload.
        3. Resolve the handler (pre-loaded map first, handler_loader fallback).
        4. Optionally hydrate an agent via constructor if agent_name is present.
        5. Invoke the handler and return the result.

        Envelope shape expected at the A2A level (JSON-RPC)
        ----------------------------------------------------
        {
            "jsonrpc": "2.0",
            "id":      "req_123",
            "method":  "a2a/request",
            "params":  {
                "message": {
                    "SendMessage": { ... }    # A2A messageType as primary key
                },
                "agent_name": "DataSteward", # optional, triggers hydration
                "profile":    { ... }        # optional, passed to constructor
            }
        }
        """
        # Step 1 - A2A protocol level
        a2a_message_type = self.get_a2a_message_type(a2a_envelope, governance_labels)
        logger.debug("A2A messageType: %s", a2a_message_type)

        # Step 2 - Semantic level
        params  = a2a_envelope.get("params", {})
        payload = params.get("message", {}).get(a2a_message_type, {})
        semantic_message_type = self.get_semantic_message_type(
            {"payload": {"message": payload}}
        )
        logger.debug("Semantic messageType: %s", semantic_message_type)

        # Step 3 - Handler resolution
        handler = self._resolve_handler(semantic_message_type)

        # Step 4 - Agent hydration
        agent_name = params.get("agent_name")
        agent      = self._hydrate_agent(agent_name, params.get("profile"))

        # Step 5 - Invocation
        if agent:
            return await handler(agent=agent, envelope=payload)
        return await handler(envelope=payload)

    # ------------------------------------------------------------------
    # A2A-level discrimination
    # ------------------------------------------------------------------

    def route_a2a(
        self,
        a2a_envelope: Dict[str, Any],
        governance_labels: Optional[List[Any]] = None,
    ) -> str:
        """
        Determine and return the A2A messageType only.
        Use this when the Solicitor-General needs the type before routing.
        """
        return self.get_a2a_message_type(a2a_envelope, governance_labels)

    def get_a2a_message_type(
        self,
        a2a_envelope: Dict[str, Any],
        governance_labels: Optional[List[Any]] = None,
    ) -> str:
        """
        Determine A2A messageType from a JSON-RPC envelope.

        Fallback strategy (in order)
        ----------------------------
        1. Direct extraction - params.message is a dict whose keys are checked
           against the schema index. If exactly one match is found, it is used.
           Fast path; covers well-formed v1.0 envelopes.

        2. governanceLabels hint - any label dict carrying an "a2a_message_type"
           key is checked against the schema index. Allows callers to annotate
           ambiguous messages without schema validation overhead.

        3. Schema-based discrimination - validate params against each known schema
           until one matches. Slowest path; last resort for legacy or v0.3
           envelopes that do not follow the single-key pattern.

        Raises
        ------
        ValueError - none of the three strategies could determine the type
        """
        params  = a2a_envelope.get("params", {})
        message = params.get("message")

        # Strategy 1: direct extraction (A2A v1.0 - primary key in message dict)
        if isinstance(message, dict) and message:
            candidates = [k for k in message if k in self.a2a_schema_index]
            if len(candidates) == 1:
                return candidates[0]
            if len(candidates) > 1:
                logger.debug(
                    "Multiple A2A messageType candidates in message keys: %s - "
                    "falling through to governanceLabels",
                    candidates,
                )

        # Strategy 2: governanceLabels hint
        if governance_labels:
            for label in governance_labels:
                if isinstance(label, dict):
                    candidate = label.get("a2a_message_type")
                    if candidate and candidate in self.a2a_schema_index:
                        logger.debug(
                            "A2A messageType resolved via governanceLabels: %s",
                            candidate,
                        )
                        return candidate

        # Strategy 3: schema-based discrimination (v0.3 / legacy fallback)
        for msg_type, schema_id in self.a2a_schema_index.items():
            if self.schema_validator(schema_id, params):
                logger.debug(
                    "A2A messageType resolved via schema validation: %s", msg_type
                )
                return msg_type

        raise ValueError(
            "Unable to determine A2A messageType. "
            f"Known types: {sorted(self.a2a_schema_index)}"
        )

    # ------------------------------------------------------------------
    # Semantic-level discrimination
    # ------------------------------------------------------------------

    def route_semantic(self, envelope: Dict[str, Any]) -> Callable:
        """
        Determine semantic messageType and return the resolved handler.
        Use this when the SG needs the handler before invoking it.
        """
        message_type = self.get_semantic_message_type(envelope)
        return self._resolve_handler(message_type)

    def get_semantic_message_type(self, envelope: Dict[str, Any]) -> str:
        """
        Extract semantic messageType from envelope["payload"]["message"].

        The message dict is expected to carry the messageType as its primary
        key, optionally alongside metadata keys. The first key that matches
        a registered messageType or capability is used. If no registered key
        is found, the first key is returned and handler resolution will fail
        loudly if it is not registered.

        Raises
        ------
        ValueError - payload.message is absent or not a dict
        """
        payload = envelope.get("payload", {})
        message = payload.get("message")

        if not isinstance(message, dict) or not message:
            raise ValueError(
                "envelope.payload.message must be a non-empty dict. "
                f"Got: {type(message).__name__}"
            )

        # Prefer a key that is already registered
        for key in message:
            if key in self.message_type_map or key in self.capability_map:
                return key

        # Fall back to first key and let handler resolution fail loudly
        first = next(iter(message))
        logger.warning(
            "No registered messageType found in message keys %s - "
            "using first key '%s'; handler resolution may fail.",
            list(message.keys()),
            first,
        )
        return first

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def registered_capabilities(self) -> List[str]:
        return sorted(self.capability_map)

    def registered_message_types(self) -> List[str]:
        return sorted(self.message_type_map)

    def registered_constructors(self) -> List[str]:
        return sorted(self.agent_constructors)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_handler(self, message_type: str) -> Callable:
        """
        Return the handler for a semantic messageType.

        Lookup order
        ------------
        1. message_type_map  (pre-loaded from YAML - preferred)
        2. capability_map    (pre-loaded from YAML)
        3. handler_loader    (SG-provided runtime fallback)
        """
        if message_type in self.message_type_map:
            return self.message_type_map[message_type]

        if message_type in self.capability_map:
            return self.capability_map[message_type]

        # Runtime fallback - let the SG's loader try
        try:
            return self.handler_loader(message_type)
        except Exception as exc:
            raise CapabilityResolutionError(
                f"No handler found for messageType '{message_type}'. "
                f"Registered messageTypes: {self.registered_message_types()}. "
                f"Registered capabilities: {self.registered_capabilities()}. "
                f"handler_loader also failed: {exc}"
            ) from exc

    def _hydrate_agent(
        self,
        agent_name: Optional[str],
        profile: Optional[Dict[str, Any]],
    ) -> Optional[Any]:
        """
        Instantiate an agent via its registered constructor, if one exists.
        Returns None if agent_name is absent or has no registered constructor.
        """
        if not agent_name:
            return None
        constructor = self.agent_constructors.get(agent_name)
        if not constructor:
            logger.debug(
                "No constructor registered for agent_name '%s' - skipping hydration.",
                agent_name,
            )
            return None
        return constructor(profile=profile)

    @staticmethod
    def _import(dotted: str, context: str = "") -> Callable:
        """
        Resolve a dotted import path to a callable at startup.

            "agents.data_steward.profile.profile_patch_handler"
            -> importlib.import_module("agents.data_steward.profile")
               .profile_patch_handler

        Raises
        ------
        CapabilityResolutionError - module not found or attribute missing
        """
        if "." not in dotted:
            raise CapabilityResolutionError(
                f"[{context}] Handler '{dotted}' is not a dotted import path. "
                f"Use 'mypackage.module.{dotted}' instead."
            )

        module_path, attr = dotted.rsplit(".", 1)
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError as exc:
            raise CapabilityResolutionError(
                f"[{context}] Cannot import module '{module_path}': {exc}"
            ) from exc

        if not hasattr(module, attr):
            raise CapabilityResolutionError(
                f"[{context}] Module '{module_path}' has no attribute '{attr}'"
            )
        return getattr(module, attr)
