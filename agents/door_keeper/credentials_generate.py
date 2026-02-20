# agents/door_keeper/credentials_generate.py

async def run(envelope, context):
    """
    Capability: Credentials.Generate
    Stub: generates credentials for agents/subscribers.
    """

    payload = envelope.get("payload", {})
    subjectId = payload.get("subjectId")

    return {
        "message": "Stub credential generation.",
        "subjectId": subjectId,
        "credentials": {"apiKey": "stub-key-xyz"},
        "correlationId": envelope.get("correlationId"),
    }
