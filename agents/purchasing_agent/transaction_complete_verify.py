# agents/purchasing_agent/transaction_complete_verify.py

async def run(envelope, context):
    """
    Capability: Transaction-Complete.Verify
    Stub: verifies a transaction.
    """

    transactionId = envelope.get("payload", {}).get("transactionId")

    return {
        "message": "Stub transaction verification.",
        "transactionId": transactionId,
        "verified": True,
        "correlationId": envelope.get("correlationId"),
    }
