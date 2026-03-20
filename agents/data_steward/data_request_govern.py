# agents/data_steward/data_request_govern.py

"""
Capability: Data-Request.Govern
Evaluates intended use of personal data before granting vault access.
The governance gate for all data access requests.

Stage: Stub — always approves. Policy evaluation deferred to Decision-Master.
Next:  Route to Decision-Master for policy evaluation when available.
       Integrate with VaultAdapter for actual data governance enforcement.
"""


async def run(payload: dict, agent_ctx, capability_ctx) -> dict:
    """
    Args:
      payload       — { "intendedUse": str, "requestedFields": [...], ... }
      agent_ctx     — AgentContext | None (governance, startup_mode, caller)
      capability_ctx — CapabilityContext | None (slim, dry_run, trace, workflow state)

    Governance note:
      This capability is the access control gate for personal data.
      In production, agent_ctx.governance_labels and agent_ctx.caller
      should be evaluated before approving any data request.
      Dry-run mode (capability_ctx.dry_run) should always be supported
      for policy testing without side effects.
    """

    intended_use = payload.get("intendedUse")
    requested_fields = payload.get("requestedFields", [])

    correlation_id = None
    task_id = None
    profile = None
    dry_run = False
    caller = None

    if capability_ctx is not None:
        correlation_id = capability_ctx.resolve("correlation_id", agent_ctx)
        task_id = capability_ctx.resolve("task_id", agent_ctx) or correlation_id
        profile = capability_ctx.resolve("profile", agent_ctx)
        dry_run = capability_ctx.dry_run

    if agent_ctx is not None:
        caller = agent_ctx.caller

    return {
        "capability": "Data-Request.Govern",
        "status": "stub",
        "message": "Stub data request governance decision.",
        "intendedUse": intended_use,
        "requestedFields": requested_fields,
        "approved": not dry_run,    # dry_run always returns unapproved
        "reason": "dry_run: approval withheld" if dry_run else "Stub policy approval.",
        "subjectProfile": profile,
        "caller": caller,
        "correlationId": correlation_id,
        "taskId": task_id,
    }
