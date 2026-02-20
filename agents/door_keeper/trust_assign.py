# agents/door_keeper/trust_assign.py

async def run(envelope, context):
    """
    Capability: Trust.Assign
    Stub: assigns a trust tier to a visitor.
    """

    payload = envelope.get("payload", {})
    visitorId = payload.get("visitorId")

    return {
        "message": "Stub trust assignment.",
        "visitorId": visitorId,
        "trustTier": "tier-1",
        "correlationId": envelope.get("correlationId"),
    }
