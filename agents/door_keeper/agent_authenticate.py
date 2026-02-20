# agents/door_keeper/agent_authenticate.py

async def run(envelope, context):
    """
    Capability: Agent.Authenticate
    Stub: authenticates an agent.
    """

    payload = envelope.get("payload", {})
    agentId = payload.get("agentId")

    return {
        "message": "Stub agent authentication.",
        "agentId": agentId,
        "authenticated": True,
        "correlationId": envelope.get("correlationId"),
    }
