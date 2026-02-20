# agents/door_keeper/agent_register.py

async def run(envelope, context):
    """
    Capability: Agent.Register
    Stub: registers a new agent.
    """

    payload = envelope.get("payload", {})
    agentName = payload.get("agentName")

    return {
        "message": "Stub agent registration.",
        "agentName": agentName,
        "status": "registered",
        "agentId": "stub-agent-456",
        "correlationId": envelope.get("correlationId"),
    }
