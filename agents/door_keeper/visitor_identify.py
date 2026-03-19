# agents/door_keeper/visitor_identify.py

async def run(payload, agent_ctx, capability_ctx):
    """
    Capability: Visitor.Identify
    Identifies a platform visitor and returns a basic profile snapshot.

    Decision signals returned here feed downstream capabilities:
      - Trust.Assign  (uses identitySource, priorVisits, riskSignals)
      - Subscriber.Register / Agent.Register (uses identifiedAs, email)

    Args:
        payload       (dict): Pre-extracted capability input.
        agent_ctx     (AgentContext): Governance context — caller, subject_ref,
                          correlation_id, governance_labels, task_id.
        capability_ctx (CapabilityContext): Execution context — dry_run, trace,
                          startup_mode.
    """

    visitor_id      = payload.get("visitorId")
    identity_source = payload.get("identitySource")   # e.g. "api-key", "mtls", "anonymous"
    ip_address      = payload.get("ipAddress")
    user_agent      = payload.get("userAgent")
    prior_visits    = payload.get("priorVisits", 0)
    risk_signals    = payload.get("riskSignals", [])

    result = {
        "visitorId":      visitor_id,
        "identifiedAs":   payload.get("identifiedAs"),
        "identitySource": identity_source,
        "ipAddress":      ip_address,
        "userAgent":      user_agent,
        "priorVisits":    prior_visits,
        "riskSignals":    risk_signals,
        "trustTier":      "unknown",   # Set by Trust.Assign — not determined here
        "identified":     visitor_id is not None,
        "correlationId":  agent_ctx.correlation_id,
        "taskId":         agent_ctx.task_id,
        "dryRun":         capability_ctx.dry_run,
        "status":         "stub",
    }

    agent_ctx.log(
        event_type="Visitor.Identify",
        message="Visitor identification attempted.",
        data={
            "visitorId":      visitor_id,
            "identitySource": identity_source,
            "identified":     result["identified"],
            "priorVisits":    prior_visits,
            "riskSignals":    risk_signals,
            "dryRun":         capability_ctx.dry_run,
            "correlationId":  agent_ctx.correlation_id,
            "taskId":         agent_ctx.task_id,
        }
    )

    return result
