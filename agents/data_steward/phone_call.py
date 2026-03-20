# agents/data_steward/phone_call.py

"""
Capability: Phone.Call
Outbound phone call for verification, negotiation, or rights requests.
Placed on behalf of the represented subject (self.profile).

Stage: Stub — returns deterministic response.
Next:  Replace with outbound call integration (e.g. Twilio, AP2 adapter).
"""


async def run(payload: dict, agent_ctx, capability_ctx) -> dict:
    """
    Args:
      payload       — { "to": str, "message": str, ... }
      agent_ctx     — AgentContext | None (governance, startup_mode, caller)
      capability_ctx — CapabilityContext | None (slim, dry_run, trace, workflow state)

    Convenience properties on self (the DataSteward instance):
      self.profile        — the person placing the call
      self.correlation_id — request correlation handle
      self.task_id        — A2A task identifier
      self.instance_id    — "Data-Steward.<profile.name>"

    Note: self is not available here — it lives on the DataSteward instance.
    Profile and correlation are passed through agent_ctx and capability_ctx
    and resolved via capability_ctx.resolve() when needed outside the agent.
    Inside the agent, use self.profile, self.correlation_id, self.task_id directly.
    """

    to = payload.get("to")
    message = payload.get("message")

    # Profile is resolved on the agent instance (self.profile) before run() is called.
    # For standalone testing, resolve from contexts if available.
    profile = None
    correlation_id = None
    task_id = None

    if capability_ctx is not None:
        profile = capability_ctx.resolve("profile", agent_ctx)
        correlation_id = capability_ctx.resolve("correlation_id", agent_ctx)
        task_id = capability_ctx.resolve("task_id", agent_ctx) or correlation_id

    return {
        "capability": "Phone.Call",
        "status": "stub",
        "message": "Stub outbound phone call placed.",
        "to": to,
        "content": message,
        "callerProfile": profile,
        "correlationId": correlation_id,
        "taskId": task_id,
    }
