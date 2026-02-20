# agents/purchasing_agent/payment_cancel.py

async def run(envelope, context):
    """
    Capability: Payment.Cancel
    Stub: cancels a payment.
    """

    paymentId = envelope.get("payload", {}).get("paymentId")

    return {
        "message": "Stub payment cancellation.",
        "paymentId": paymentId,
        "status": "cancelled",
        "correlationId": envelope.get("correlationId"),
    }
