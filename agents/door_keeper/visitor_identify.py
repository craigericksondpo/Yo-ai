# agents/door_keeper/visitor_identify.py

async def run(envelope, context):
    """
    Capability: Visitor.Identify
    Stub: identifies a visitor and returns a basic profile.
    """

    payload = envelope.get("payload", {})
    visitorId = payload.get("visitorId")

    return {
        "message": "Stub visitor identification.",
        "visitorId": visitorId,
        "identified": True,
        "trustTier": "unknown",
        "correlationId": envelope.get("correlationId"),
    }
