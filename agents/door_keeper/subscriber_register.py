# agents/door_keeper/subscriber_register.py

async def run(payload, agent_ctx, capability_ctx):
    """
    Capability: Subscriber.Register
    Registers a new subscriber and issues a RegisteredSubscriber card.

    Registration criteria (Yo-ai Agent Registry):
      - Named individual — not a group email (e.g. legal@company.com rejected)
      - Accountable representative of the provider organization
      - Recommended: corporate officer or legal representative authorized
        to sign binding agreements

    Args:
        payload        (dict): Pre-extracted capability input.
        agent_ctx      (AgentContext): Governance context.
        capability_ctx (CapabilityContext): Execution context — dry_run, trace.
    """

    email        = payload.get("email")
    name         = payload.get("name")
    organization = payload.get("organization")
    role         = payload.get("role")           # e.g. "corporate-officer", "legal-rep"
    provider_url = payload.get("providerUrl")

    # Stub validation note: real implementation rejects group/anonymous emails
    # and verifies named individual against provider formation documents.
    is_group_email = email and any(
        email.lower().startswith(prefix)
        for prefix in ("legal@", "info@", "admin@", "contact@", "support@")
    )

    result = {
        "subscriberId":   "stub-subscriber-123",
        "email":          email,
        "name":           name,
        "organization":   organization,
        "role":           role,
        "providerUrl":    provider_url,
        "status":         "registered",
        "warning":        "group-email-detected" if is_group_email else None,
        "correlationId":  agent_ctx.correlation_id,
        "taskId":         agent_ctx.task_id,
        "dryRun":         capability_ctx.dry_run,
        "stub":           True,
    }

    agent_ctx.log(
        event_type="Subscriber.Register",
        message="Subscriber registration attempted.",
        data={
            "email":         email,
            "name":          name,
            "organization":  organization,
            "role":          role,
            "isGroupEmail":  is_group_email,
            "status":        result["status"],
            "dryRun":        capability_ctx.dry_run,
            "correlationId": agent_ctx.correlation_id,
            "taskId":        agent_ctx.task_id,
        }
    )

    return result
