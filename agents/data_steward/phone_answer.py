# agents/data_steward/phone_answer.py

"""
Capability: Phone.Answer
Inbound call handling — caller verification and purpose detection.
Answers on behalf of the represented subject (self.profile).

Stage: Stub — returns deterministic response.
Next:  Replace with inbound call integration and caller verification logic.
       Consider routing to Just-Ask for unknown callers.
"""


async def run(payload: dict, agent_ctx, capability_ctx) -> dict:
    """
    Args:
      payload       — { "callerId": str, ... }
      agent_ctx     — AgentContext | None (governance, startup_mode, caller)
      capability_ctx — CapabilityContext | None (slim, dry_run, trace, workflow state)
    """

    caller_id = payload.get("callerId")

    correlation_id = None
    task_id = None
    startup_mode = None

    if capability_ctx is not None:
        correlation_id = capability_ctx.resolve("correlation_id", agent_ctx)
        task_id = capability_ctx.resolve("task_id", agent_ctx) or correlation_id

    if agent_ctx is not None:
        startup_mode = agent_ctx.startup_mode

    return {
        "capability": "Phone.Answer",
        "status": "stub",
        "message": "Stub inbound call answered.",
        "callerId": caller_id,
        "verified": True,
        "purpose": "stubbed-purpose",
        "startupMode": startup_mode,
        "correlationId": correlation_id,
        "taskId": task_id,
    }
