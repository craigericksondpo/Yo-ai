# agents/door_keeper/subscriber_authenticate.py

async def run(envelope, context):
    """
    Capability: Subscriber.Authenticate
    Stub: authenticates a subscriber.
    """

    payload = envelope.get("payload", {})
    subscriberId = payload.get("subscriberId")

    return {
        "message": "Stub subscriber authentication.",
        "subscriberId": subscriberId,
        "authenticated": True,
        "correlationId": envelope.get("correlationId"),
    }
