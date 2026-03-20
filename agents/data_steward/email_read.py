# agents/data_steward/email_read.py

"""
Capability: Email.Read
Reads inbound email, detects spam/phishing, extracts workflow triggers.
Reads on behalf of the represented subject (self.profile).

Stage: Stub — returns deterministic response.
Next:  Replace with email provider integration (Gmail, Outlook, etc.)
       Add real spam/phishing detection.
       Extract workflow triggers for downstream capabilities.
"""


async def run(payload: dict, agent_ctx, capability_ctx) -> dict:
    """
    Args:
      payload       — { "email": str | dict, "folder": str, ... }
      agent_ctx     — AgentContext | None (governance, startup_mode, caller)
      capability_ctx — CapabilityContext | None (slim, dry_run, trace, workflow state)
    """

    email = payload.get("email")
    folder = payload.get("folder", "inbox")

    correlation_id = None
    task_id = None
    dry_run = False

    if capability_ctx is not None:
        correlation_id = capability_ctx.resolve("correlation_id", agent_ctx)
        task_id = capability_ctx.resolve("task_id", agent_ctx) or correlation_id
        dry_run = capability_ctx.dry_run

    return {
        "capability": "Email.Read",
        "status": "stub",
        "message": "Stub email read.",
        "email": email,
        "folder": folder,
        "spam": False,
        "phishing": False,
        "workflowTrigger": None if dry_run else "stubbed-trigger",
        "correlationId": correlation_id,
        "taskId": task_id,
    }
