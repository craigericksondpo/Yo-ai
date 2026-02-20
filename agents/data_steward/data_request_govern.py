# agents/data_steward/data_request_govern.py

async def run(envelope, context):
    """
    Capability: Data-Request.Govern
    Stub: evaluates intended use of personal data.
    """

    payload = envelope.get("payload", {})
    intendedUse = payload.get("intendedUse")

    return {
        "message": "Stub data request governance decision.",
        "intendedUse": intendedUse,
        "approved": True,
        "reason": "Stub policy approval.",
        "subjectProfile": context.profile,
        "correlationId": envelope.get("correlationId"),
    }
