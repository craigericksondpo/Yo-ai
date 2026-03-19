# agents/door_keeper/accessrights_manage.py

async def run(payload, agent_ctx, capability_ctx):
    """
    Capability: AccessRights.Manage
    Manages access rights for RegisteredAgents and RegisteredSubscribers.

    Backed by the AccessAdministrator tool in production:
      - Provider: Apache Kafka 3.7.0
      - Config: bootstrapServers=kafka:9092, securityProtocol=SASL_SSL
      - Capabilities: grant, revoke, issue-credentials
      - Path: /access_admin.py
    (See Door-Keeper-ExtendedAgentCard.md — AccessAdministrator tool artifact)

    Actions:
      grant   — grants access to a resource or Kafka topic
      revoke  — revokes existing access
      inspect — returns current access rights for a subject

    Subject types: RegisteredAgent | RegisteredSubscriber | Visitor

    Args:
        payload        (dict): Pre-extracted capability input.
        agent_ctx      (AgentContext): Governance context.
        capability_ctx (CapabilityContext): Execution context — dry_run, trace.
    """

    subject_id    = payload.get("subjectId")
    subject_type  = payload.get("subjectType")    # "RegisteredAgent" | "RegisteredSubscriber" | "Visitor"
    action        = payload.get("action")         # "grant" | "revoke" | "inspect"
    resource      = payload.get("resource")       # e.g. Kafka topic, capability name, endpoint
    permissions   = payload.get("permissions", []) # e.g. ["read", "write", "post"]
    rationale     = payload.get("rationale")

    result = {
        "subjectId":     subject_id,
        "subjectType":   subject_type,
        "action":        action,
        "resource":      resource,
        "permissions":   permissions,
        "rationale":     rationale,
        "outcome":       "updated",   # "updated" | "denied" | "no-change"
        "correlationId": agent_ctx.correlation_id,
        "taskId":        agent_ctx.task_id,
        "dryRun":        capability_ctx.dry_run,
        "status":        "stub",
    }

    agent_ctx.log(
        event_type="AccessRights.Manage",
        message=f"Access rights {action} attempted.",
        data={
            "subjectId":     subject_id,
            "subjectType":   subject_type,
            "action":        action,
            "resource":      resource,
            "permissions":   permissions,
            "rationale":     rationale,
            "outcome":       result["outcome"],
            "dryRun":        capability_ctx.dry_run,
            "correlationId": agent_ctx.correlation_id,
            "taskId":        agent_ctx.task_id,
        }
    )

    return result
