# agents/solicitor_general/just_ask.py

async def run(envelope, context):
    """
    Implements the Solicitor-General's Just-Ask capability.

    This is the default conversational entrypoint for the platform.
    It can:
      - answer general questions
      - describe platform capabilities
      - route users to the right agent
      - provide onboarding guidance
    """

    question = envelope.get("payload", {}).get("question") or ""
    caller = envelope.get("caller", {})
    subject = envelope.get("subject", {})

    return {
        "message": "This is the Solicitor-General responding via Just-Ask.",
        "questionReceived": question,
        "caller": caller,
        "subject": subject,
        "governanceLabels": envelope.get("governanceLabels", []),
    }
