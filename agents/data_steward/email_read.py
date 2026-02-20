# agents/data_steward/email_read.py

async def run(envelope, context):
    """
    Capability: Email.Read
    Stub: reads inbound email, detects spam/phishing, extracts triggers.
    """

    payload = envelope.get("payload", {})
    email = payload.get("email")

    return {
        "message": "Stub email read.",
        "email": email,
        "spam": False,
        "phishing": False,
        "workflowTrigger": "stubbed-trigger",
        "correlationId": envelope.get("correlationId"),
    }
