# agents/door_keeper/subscriber_register.py

async def run(envelope, context):
    """
    Capability: Subscriber.Register
    Stub: registers a new subscriber.
    """

    payload = envelope.get("payload", {})
    email = payload.get("email")

    return {
        "message": "Stub subscriber registration.",
        "email": email,
        "status": "registered",
        "subscriberId": "stub-subscriber-123",
        "correlationId": envelope.get("correlationId"),
    }
