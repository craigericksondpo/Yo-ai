# agents/door_keeper/door_keeper.py

from core.platform_agent import PlatformAgent


class DoorKeeperAgent(PlatformAgent):
    """
    Door-Keeper: profiles guests, registers subscribers/agents,
    authenticates visitors, assigns trust, and manages access rights.

    Inherits from PlatformAgent → YoAiAgent → BaseAgent.

    Card is auto-loaded from agent_card/ bundle by BaseAgent.__init__().
    Constructor is keyword-only (no positional args).

    Two-context model (Gap Registry v2):
        AgentContext      — governance: caller, subject_ref, correlation_id,
                            governance_labels, task_id, startup_mode
        CapabilityContext — execution: capability_id, dry_run, trace,
                            startup_mode, task_id

    Capability dispatch pattern:
        1. Import and call run(payload, agent_ctx, capability_ctx)
        2. run() module handles all logic and logging
        3. call_ai() fallback applied by handler, not here

    This agent is profile-aware: it may operate with a subject profile
    or visitor profile depending on the request context.
    """

    def __init__(self, *, card=None, extended_card=None, slim=False):
        super().__init__(
            card=card,
            extended_card=extended_card,
            slim=slim,
        )

    # ------------------------------------------------------------------
    # Capability: Visitor.Identify
    # ------------------------------------------------------------------
    async def visitor_identify(self, payload, agent_ctx, capability_ctx):
        from .visitor_identify import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: Subscriber.Register
    # ------------------------------------------------------------------
    async def subscriber_register(self, payload, agent_ctx, capability_ctx):
        from .subscriber_register import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: Credentials.Generate
    # ------------------------------------------------------------------
    async def credentials_generate(self, payload, agent_ctx, capability_ctx):
        from .credentials_generate import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: Subscriber.Authenticate
    # ------------------------------------------------------------------
    async def subscriber_authenticate(self, payload, agent_ctx, capability_ctx):
        from .subscriber_authenticate import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: Agent.Register
    # ------------------------------------------------------------------
    async def agent_register(self, payload, agent_ctx, capability_ctx):
        from .agent_register import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: Trust.Assign
    # ------------------------------------------------------------------
    async def trust_assign(self, payload, agent_ctx, capability_ctx):
        from .trust_assign import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: AccessRights.Manage
    # ------------------------------------------------------------------
    async def accessrights_manage(self, payload, agent_ctx, capability_ctx):
        from .accessrights_manage import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Capability: Agent.Authenticate
    # ------------------------------------------------------------------
    async def agent_authenticate(self, payload, agent_ctx, capability_ctx):
        from .agent_authenticate import run
        return await run(payload, agent_ctx, capability_ctx)

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------
    def _build_agent_context(self, params: dict):
        """
        Build AgentContext (governance layer) from inbound request params.

        Uses self.context_class() — no import needed (BaseAgent provides it).

        Fields:
            caller           — identity of the calling agent/subscriber
            subject_ref      — lightweight pointer to the subject (not full data)
            profile          — resolved at construction; never from request params
            correlation_id   — request correlation chain
            task_id          — task this request belongs to
            governance_labels — platform-assigned only; caller labels ignored
            startup_mode     — a2a | direct | api | starlette
        """
        return self.context_class()(
            caller=params.get("caller"),
            subject_ref=params.get("subjectRef"),
            profile=self.profile,
            correlation_id=params.get("correlationId"),
            task_id=params.get("taskId"),
            governance_labels=[],       # platform-assigned only — never from caller
            startup_mode=params.get("startupMode", "api"),
        )

    def _build_capability_context(self, capability_id: str, params: dict):
        """
        Build CapabilityContext (execution layer) from inbound request params.

        Uses self.capability_context_class() — no import needed (BaseAgent provides it).

        Fields:
            capability_id  — canonical capability identifier (e.g. "Trust.Assign")
            dry_run        — if True, execute logic but do not persist side effects
            trace          — if True, emit OpenTelemetry trace spans (Layer 4, deferred)
            task_id        — propagated from AgentContext
            startup_mode   — propagated from AgentContext
        """
        return self.capability_context_class()(
            capability_id=capability_id,
            dry_run=params.get("dryRun", False),
            trace=params.get("trace", False),
            task_id=params.get("taskId"),
            startup_mode=params.get("startupMode", "api"),
        )
