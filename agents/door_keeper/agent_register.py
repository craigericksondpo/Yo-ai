# agents/door_keeper/agent_register.py

async def run(payload, agent_ctx, capability_ctx):
    """
    Capability: Agent.Register
    Validates an agent card and issues a RegisteredAgent card for
    qualified agents.

    Registration criteria (Yo-ai Agent Registry):
      - Must submit an A2A-compliant agent card
      - Provider must have a named RegisteredSubscriber on record
      - Agent does NOT need A2A interaction capability to register
        (platform provides the wrapper on registration)

    Outcomes emitted: registered | pending-registration | denied-agent

    Args:
        payload        (dict): Pre-extracted capability input.
        agent_ctx      (AgentContext): Governance context.
        capability_ctx (CapabilityContext): Execution context — dry_run, trace.
    """

    agent_card       = payload.get("agentCard", {})
    agent_name       = agent_card.get("name") or payload.get("agentName")
    provider         = agent_card.get("provider", {})
    subscriber_id    = payload.get("subscriberId")   # Registering human representative
    declared_skills  = agent_card.get("skills", [])

    # Stub: real implementation validates A2A compliance and subscriber record
    registration_status = "registered"
    agent_id = "stub-agent-456"
    denial_reason = None

    result = {
        "agentId":            agent_id,
        "agentName":          agent_name,
        "provider":           provider,
        "subscriberId":       subscriber_id,
        "declaredSkills":     [s.get("name") for s in declared_skills],
        "registrationStatus": registration_status,   # registered | pending-registration | denied-agent
        "denialReason":       denial_reason,
        "correlationId":      agent_ctx.correlation_id,
        "taskId":             agent_ctx.task_id,
        "dryRun":             capability_ctx.dry_run,
        "status":             "stub",
    }

    agent_ctx.log(
        event_type="Agent.Register",
        message="Agent registration attempted.",
        data={
            "agentName":          agent_name,
            "provider":           provider,
            "subscriberId":       subscriber_id,
            "declaredSkillCount": len(declared_skills),
            "registrationStatus": registration_status,
            "denialReason":       denial_reason,
            "dryRun":             capability_ctx.dry_run,
            "correlationId":      agent_ctx.correlation_id,
            "taskId":             agent_ctx.task_id,
        }
    )

    return result
