# agents/purchasing_agent/budget_check.py

"""
Capability: Budget.Check
Stub — always returns 1000. Next: fetch real balance from vault/budget store.
      Returns indeterminate status when profile is None (anonymous caller).
"""


async def run(payload: dict, agent_ctx, capability_ctx) -> dict:
    """
    Args:
      payload       — capability-specific input fields
      agent_ctx     — AgentContext | None  (governance, startup_mode, caller)
      capability_ctx — CapabilityContext | None  (slim, dry_run, trace, workflow state)
    """
    amount = payload.get("amount")
    currency = payload.get("currency")

    profile = None
    correlation_id = None
    task_id = None
    dry_run = False

    if capability_ctx is not None:
        profile = capability_ctx.resolve("profile", agent_ctx)
        correlation_id = capability_ctx.resolve("correlation_id", agent_ctx)
        task_id = capability_ctx.resolve("task_id", agent_ctx) or correlation_id
        dry_run = capability_ctx.dry_run

    return {
        "capability": "Budget.Check",
        "message": "Stub Budget.Check response.",
        "eligible": profile is not None,
        "availableBudget": 1000 if profile is not None else None,
        "amount": amount,
        "currency": currency,
        "status": "available" if profile is not None else "indeterminate",
        "reason": None if profile is not None else "No subject profile provided.",
        "required": None if profile is not None else ["profile"],

        "subjectProfile": profile,
        "correlationId": correlation_id,
        "taskId": task_id,
    }
