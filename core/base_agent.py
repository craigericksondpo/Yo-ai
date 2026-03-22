# core/base_agent.py

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Literal


# ----------------------------------------------------------------------
# Semantic execution context — platform governance layer
# ----------------------------------------------------------------------
class AgentContext:
    """
    AgentContext:
    Platform governance context constructed by the Solicitor-General.

    Travels through the A2A routing pipeline:
      A2ATransport → SG → UCR → capability handler → run()

    This is NOT a transport envelope and NOT a capability execution context.
    Transport envelopes are parsed by A2ATransport.
    Capability execution context is carried by CapabilityContext.

    AgentContext answers: WHO is asking, ON WHOSE BEHALF, under WHAT
    governance conditions, HOW WAS IT INVOKED, and HOW DO WE TRACE IT?

    AgentContext is not imported directly by subclasses. It is exposed
    as BaseAgent.context_class so the full inheritance chain can reference
    it without a separate import.

    Fields:

      Correlation and task identity:
        correlation_id  — JSON-RPC id. Primary request-response handle.
                          Set by A2ATransport at the protocol boundary.
        task_id         — A2A task identifier. May differ from correlation_id.
                          For external callers: their task_id, returned in
                          metadata.taskID. Defaults to correlation_id if absent.
        instance_id     — Runtime identity of the agent instance handling this
                          request. Format: actor_name [+ "." + profile.name
                          [+ "-" + counter]]. Set by SG after registration.
                          None for PlatformAgents (they don't represent people).

      Startup mode:
        startup_mode    — How the capability was invoked. Set by the transport
                          layer before passing to the SG. Used for audit,
                          debugging, and governance trail interpretation.
                          Values: "a2a" | "direct" | "api" | "starlette"

      Caller identity:
        caller          — Identity of the agent or user who sent the request.
                          Present for registered callers, None for anonymous.
                          Used by showCard() for trust-gated card access.
                          Used by the Door-Keeper for identity evaluation.

      Subject reference:
        subject_ref     — Lightweight pointer to the subject of the request.
                          Informational only — does not drive routing decisions.
                          Distinct from profile: profile is loaded validated data;
                          subject_ref is a lightweight reference tag.

      Profile:
        profile         — The person or org the agent represents for this request.
                          Drives instance identity, vault access, and governance.
                          Extracted from the envelope by the SG.
                          None for PlatformAgents.
        profile_patch   — Runtime modifications to the resolved profile.

      Governance:
        governance_labels — Platform-assigned outbound labels only.
                            NEVER populated from caller-supplied input.
                            Carries agent, capability, task_id lineage tags.
                            Persists and flows to downstream agents and processes.
                            Format: ["agent:Data-Steward",
                                     "capability:Budget.Check",
                                     "task_id:vm-abc-corp-001"]

    Resolution order (when both contexts are present):
      CapabilityContext > AgentContext > BaseAgent defaults
      Fields present in CapabilityContext take priority over AgentContext.
      Use CapabilityContext.resolve(field, agent_context) for resolution.
    """

    # Valid startup mode values
    STARTUP_MODES = frozenset({"a2a", "direct", "api", "starlette"})

    def __init__(
        self,
        *,
        # Correlation and task identity
        correlation_id: str | None = None,
        task_id: str | None = None,
        instance_id: str | None = None,
        # Startup mode
        startup_mode: str | None = None,
        # Caller identity
        caller: dict | None = None,
        # Subject reference
        subject_ref: dict | None = None,
        # Profile
        profile: dict | None = None,
        profile_patch: dict | None = None,
        # Governance
        governance_labels: list[str] | None = None,
    ):
        self.correlation_id = correlation_id
        # task_id defaults to correlation_id if not explicitly supplied
        self.task_id = task_id if task_id is not None else correlation_id
        self.instance_id = instance_id
        self.startup_mode = startup_mode
        self.caller = caller
        self.subject_ref = subject_ref
        self.profile = profile
        self.profile_patch = profile_patch
        self.governance_labels = governance_labels or []

    def to_dict(self) -> dict:
        """
        Serialize to a plain dict — for logging and diagnostics.
        """
        return {
            "correlation_id": self.correlation_id,
            "task_id": self.task_id,
            "instance_id": self.instance_id,
            "startup_mode": self.startup_mode,
            "caller": self.caller,
            "subject_ref": self.subject_ref,
            "profile": self.profile,
            "profile_patch": self.profile_patch,
            "governance_labels": self.governance_labels,
        }


# ----------------------------------------------------------------------
# Capability execution context — the baton in the relay race
# ----------------------------------------------------------------------
class CapabilityContext:
    """
    CapabilityContext:
    Capability execution context — carries everything a capability needs
    to execute correctly regardless of how it was invoked.

    Constructed by whoever is invoking the capability:
      - SG: from capability_map entry + envelope fields (Mode A)
      - Workflow-Builder: from workflow step definition
      - Direct API handler: from request body capability_ctx block (Mode B)
      - Test harness: minimal construction

    CapabilityContext answers: WHAT does this capability need to run?

    Resolution order (highest to lowest priority):
      CapabilityContext > AgentContext > BaseAgent defaults

    Fields with matching names in both contexts resolve from
    CapabilityContext first, falling back to AgentContext.
    Use resolve(field, agent_context) for safe resolution.

    CapabilityContext is not imported directly by subclasses. It is exposed
    as BaseAgent.capability_context_class so the full inheritance chain can
    reference it without a separate import.

    Execution configuration fields (CapabilityContext only — never on AgentContext):
      slim     — skip expensive init (fingerprints, knowledge, tools)
      tools    — selective tool loading: None=all, []=none, ["vault"]=named
      dry_run  — validate without executing side effects
      trace    — activate OTel Layer 4 explainability tracing

    Identity override fields (override AgentContext when set):
      correlation_id, task_id, instance_id
      profile, profile_patch, caller, subject_ref

    Workflow state fields:
      step, prior_outputs, state
    """

    def __init__(
        self,
        *,
        # --- Capability identity ---
        capability_id: str | None = None,

        # --- Execution configuration (CapabilityContext only) ---
        slim: bool = False,
        tools: list[str] | None = None,
        dry_run: bool = False,
        trace: bool = False,
        startup_mode: str | None = None,

        # --- Identity and correlation (override AgentContext if set) ---
        correlation_id: str | None = None,
        task_id: str | None = None,
        instance_id: str | None = None,

        # --- Subject context (override AgentContext if set) ---
        profile: dict | None = None,
        profile_patch: dict | None = None,
        caller: dict | None = None,
        subject_ref: dict | None = None,

        # --- Workflow state ---
        step: int | None = None,
        prior_outputs: dict | None = None,
        state: dict | None = None,
    ):
        # Capability identity
        self.capability_id = capability_id
        self.startup_mode = startup_mode

        # Execution configuration
        self.slim = slim
        self.tools = tools
        self.dry_run = dry_run
        self.trace = trace

        # Identity and correlation
        self.correlation_id = correlation_id
        self.task_id = task_id
        self.instance_id = instance_id

        # Subject context
        self.profile = profile
        self.profile_patch = profile_patch
        self.caller = caller
        self.subject_ref = subject_ref

        # Workflow state
        self.step = step
        self.prior_outputs = prior_outputs or {}
        self.state = state or {}

    # ------------------------------------------------------------------
    # Schema name properties (from patch: base_agent_capability_context_patch.py)
    # ------------------------------------------------------------------
    @property
    def input_schema_name(self) -> str:
        """
        Canonical input schema filename for this capability.

        Derived deterministically from capability_id:
            "Trust.Assign"  →  "trust.assign.input.schema.json"

        Use as event_type in Agent Log Entry 1 (capability received):
            agent_ctx.log(event_type=capability_ctx.input_schema_name, ...)

        Matches filenames in training/artifacts/messages/ and
        $ref URLs in agent cards and extended cards.
        Returns empty string if capability_id is not set.
        """
        if not self.capability_id:
            return ""
        return f"{self.capability_id.lower()}.input.schema.json"

    @property
    def output_schema_name(self) -> str:
        """
        Canonical output schema filename for this capability.

        Derived deterministically from capability_id:
            "Trust.Assign"  →  "trust.assign.output.schema.json"

        Use as event_type in Agent Log Entry 2 (capability completed):
            agent_ctx.log(event_type=capability_ctx.output_schema_name, ...)

        Matches filenames in training/artifacts/messages/ and
        $ref URLs in agent cards and extended cards.
        Returns empty string if capability_id is not set.
        """
        if not self.capability_id:
            return ""
        return f"{self.capability_id.lower()}.output.schema.json"

    # ------------------------------------------------------------------
    # Context resolution helper
    # ------------------------------------------------------------------
    def resolve(self, field: str, agent_context=None, default=None):
        """
        Resolve a field using priority order:
          CapabilityContext → AgentContext → default

        CapabilityContext wins when its field is not None.
        Falls back to AgentContext, then to the supplied default.

        Use inside run(payload, agent_context, capability_ctx):

            profile = capability_ctx.resolve("profile", agent_context)
            correlation_id = capability_ctx.resolve("correlation_id", agent_context)
            task_id = capability_ctx.resolve("task_id", agent_context)
            startup_mode = capability_ctx.resolve("startup_mode", agent_context)

        Execution-configuration fields (slim, tools, dry_run, trace)
        are CapabilityContext-only and do not need resolution.
        """
        cap_val = getattr(self, field, None)
        if cap_val is not None:
            return cap_val

        if agent_context is not None:
            agent_val = getattr(agent_context, field, None)
            if agent_val is not None:
                return agent_val

        return default

    @classmethod
    def from_dict(cls, data: dict) -> "CapabilityContext":
        """
        Construct from a plain dict — used by api_handler.py and
        solicitor_general_handler.py to parse the capability_ctx block
        from a Mode B / Mode 3 request body.
        Unknown keys are silently ignored — forward compatible.
        """
        return cls(
            capability_id=data.get("capability_id"),
            slim=data.get("slim", False),
            tools=data.get("tools"),
            dry_run=data.get("dry_run", False),
            trace=data.get("trace", False),
            startup_mode=data.get("startup_mode"),
            correlation_id=data.get("correlation_id"),
            task_id=data.get("task_id"),
            instance_id=data.get("instance_id"),
            profile=data.get("profile"),
            profile_patch=data.get("profile_patch"),
            caller=data.get("caller"),
            subject_ref=data.get("subject_ref"),
            step=data.get("step"),
            prior_outputs=data.get("prior_outputs"),
            state=data.get("state"),
        )

    def to_dict(self) -> dict:
        """
        Serialize to a plain dict — for logging, envelope passthrough,
        and workflow state persistence.
        """
        return {
            "capability_id": self.capability_id,
            "startup_mode": self.startup_mode,
            "slim": self.slim,
            "tools": self.tools,
            "dry_run": self.dry_run,
            "trace": self.trace,
            "correlation_id": self.correlation_id,
            "task_id": self.task_id,
            "instance_id": self.instance_id,
            "profile": self.profile,
            "profile_patch": self.profile_patch,
            "caller": self.caller,
            "subject_ref": self.subject_ref,
            "step": self.step,
            "prior_outputs": self.prior_outputs,
            "state": self.state,
        }


# ----------------------------------------------------------------------
# BaseAgent: shared runtime behavior for platform-native agents
# ----------------------------------------------------------------------
class BaseAgent:
    """
    BaseAgent:
    Concrete base class for YoAiAgent, PlatformAgent, and VisitingAgent wrappers.

    Responsibilities:
      - Load agent cards from the agent_card/ folder in the deployment bundle
      - Provide identity fields (name, capabilities)
      - Provide showCard() — trust-gated card exposure helper
      - Provide a safe handle_request() wrapper
      - Provide JSON-RPC error normalization
      - Provide a capability lookup helper

    Context classes exposed as class attributes:
      context_class            → AgentContext
      capability_context_class → CapabilityContext

    Both are accessible throughout the inheritance chain without imports.
    Subclasses construct contexts via self.context_class(...) and
    self.capability_context_class(...).

    Card Loading:
      Cards are loaded automatically from the agent's bundle at construction.
      Both cards are always optional — missing files degrade gracefully to {}.
      VisitingAgents have no bundle and will always have card = {}.

      Layout (relative to the agent's module file):
        agent_card/
          agent.json          ← public A2A basic card
          extended/
            agent.json        ← authenticated extended card (optional)

    showCard():
      A helper method (not a routable capability) that returns the appropriate
      card based on caller context. Defined here on BaseAgent and overridden
      by YoAiAgent and PlatformAgent. Documented in the Developer Guide.

      If no card is available, fires a NO_CARD alert event — three bells —
      to the platform log. This event is intended for the Kafka Observability
      Publisher to route to the Door-Keeper's GuestRegistry topic.
    """

    # Both context classes exposed as class attributes so the full
    # inheritance chain can reference them without importing directly.
    context_class = AgentContext
    capability_context_class = CapabilityContext

    def __init__(
        self,
        *,
        card: dict | None = None,
        extended_card: dict | None = None,
        context: AgentContext | None = None,
    ):
        # ------------------------------------------------------------------
        # Card loading — from agent_card/ in the deployment bundle.
        # Caller-supplied card/extended_card take precedence if provided.
        # Falls back to filesystem load, then gracefully to {}.
        # VisitingAgents have no bundle — both will be {}.
        # ------------------------------------------------------------------
        self.card = card if card is not None else self._load_card("agent_card/agent.json")
        self.extended = (
            extended_card if extended_card is not None
            else self._load_card("agent_card/extended/agent.json")
        )

        self.context = context  # semantic context, may be None at init

        # Identity is card-driven
        self.name = self.card.get("name", "unknown-agent") if self.card else "unknown-agent"

        self.default_role = "ROLE_AGENT"

        # Capabilities declared in the card(s)
        caps = list((self.card or {}).get("capabilities", []))
        if self.extended:
            caps += self.extended.get("capabilities", [])
        self.capabilities = caps

    # ------------------------------------------------------------------
    # Card loader — graceful filesystem reader
    # ------------------------------------------------------------------
    def _load_card(self, relative_path: str) -> dict:
        """
        Load a JSON card file from a path relative to this agent's
        module file. Returns {} on any failure — never raises.
        """
        try:
            module_dir = Path(__file__).resolve().parent
            card_path = module_dir / relative_path
            if card_path.exists():
                with card_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    # ------------------------------------------------------------------
    # showCard() — trust-gated card exposure helper
    # ------------------------------------------------------------------
    def showCard(self, context: AgentContext | None = None) -> dict:
        """
        Return the appropriate agent card based on caller context.

        BaseAgent default: returns basic card, fires NO_CARD if absent.
        Overridden by YoAiAgent (extended card for identified callers)
        and PlatformAgent (basic card only, always).

        NOT a routable capability. Documented in the Developer Guide.
        """
        if not self.card:
            self._fire_no_card_event(context)
            return {}
        return self.card

    # ------------------------------------------------------------------
    # NO_CARD alert event — three bells
    # ------------------------------------------------------------------
    def _fire_no_card_event(self, context: AgentContext | None) -> None:
        """
        Fire a NO_CARD alert event to the platform log.

        Three bells — everyone is notified, no one is blocked.
        The Kafka Observability Publisher routes this to the
        Door-Keeper's GuestRegistry topic asynchronously.
        """
        record = {
            "event_type": "no_card",
            "severity": "alert",
            "alert_bells": 3,
            "actor": self.__class__.__name__,
            "agent_name": self.name,
            "correlation_id": context.correlation_id if context else None,
            "task_id": context.task_id if context else None,
            "startup_mode": context.startup_mode if context else None,
            "caller": context.caller if context else None,
            "instance_id": context.instance_id if context else None,
            "message": (
                "NO_CARD: Agent card absent — VisitingAgent detected "
                "or card load failed. Door-Keeper notified via GuestRegistry topic."
            ),
            "topic_hint": "GuestRegistry",
        }
        try:
            logger = getattr(self, "logger", None)
            if logger and hasattr(logger, "write"):
                logger.write(record)
                return
        except Exception:
            pass
        import json as _json
        print(_json.dumps(record))

    # ------------------------------------------------------------------
    # Universal capability-execution wrapper
    # ------------------------------------------------------------------
    def handle_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        Universal capability-execution wrapper for BaseAgent / VisitingAgents.

        Invoked after the transport layer has parsed the JSON-RPC envelope.
        Provides final safety guarantees: capability lookup, error normalization,
        AnyException wrapping — no raw exceptions ever escape an agent.
        """
        from core.runtime.error_handler import ErrorHandler

        request_id = request.get("id")
        method = request.get("method")

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
    # Capability lookup helper
    # ------------------------------------------------------------------
    def get_capability(self, name: str, context: AgentContext | None = None):
        """
        Retrieve a capability handler by name.

        The optional context parameter is available to caller-aware handlers
        that behave differently based on caller identity or governance labels.

        Args:
            name:    Capability handler method name.
            context: Optional AgentContext — for caller-aware dispatch.

        Returns:
            Callable handler if found, None otherwise.
        """
        return getattr(self, name, None)
