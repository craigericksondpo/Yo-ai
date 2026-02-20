# agents/data_steward/email_send.py

async def run(envelope, context):
    """
    Capability: Email.Send
    Stub: sends outbound email on behalf of the data subject.
    """

    payload = envelope.get("payload", {})
    to = payload.get("to")
    subject = payload.get("subject")
    body = payload.get("body")

    return {
        "message": "Stub outbound email sent.",
        "to": to,
        "subject": subject,
        "body": body,
        "senderProfile": context.profile,
        "correlationId": envelope.get("correlationId"),
    }
