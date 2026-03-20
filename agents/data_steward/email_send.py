# agents/data_steward/email_send.py

"""
Capability: Email.Send
Sends outbound email on behalf of the represented subject (self.profile).

Stage: Stub — returns deterministic response.
Next:  Replace with email provider integration (Gmail, SES, Outlook, etc.)
       Add sender verification against self.profile.
       Add outbound governance check (Data-Request.Govern) for sensitive content.

Note: 'subject' renamed to 'email_subject' in payload to avoid collision
      with the reserved 'subject' field in AgentContext / CapabilityContext.
"""


async def run(payload: dict, agent_ctx, capability_ctx) -> dict:
    """
    Args:
      payload       — { "to": str, "email_subject": str, "body": str, ... }
      agent_ctx     — AgentContext | None (governance, startup_mode, caller)
      capability_ctx — CapabilityContext | None (slim, dry_run, trace, workflow state)
    """

    to = payload.get("to")
    email_subject = payload.get("email_subject") or payload.get("subject")
    body = payload.get("body")

    correlation_id = None
    task_id = None
    profile = None
    dry_run = False

    if capability_ctx is not None:
        correlation_id = capability_ctx.resolve("correlation_id", agent_ctx)
        task_id = capability_ctx.resolve("task_id", agent_ctx) or correlation_id
        profile = capability_ctx.resolve("profile", agent_ctx)
        dry_run = capability_ctx.dry_run

    return {
        "capability": "Email.Send",
        "status": "stub",
        "message": "Stub outbound email sent." if not dry_run else "Stub dry_run — email not sent.",
        "to": to,
        "email_subject": email_subject,
        "body": body,
        "senderProfile": profile,
        "sent": not dry_run,
        "correlationId": correlation_id,
        "taskId": task_id,
    }
