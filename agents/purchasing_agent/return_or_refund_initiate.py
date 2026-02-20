# agents/purchasing_agent/return_or_refund_initiate.py

async def run(envelope, context):
    """
    Capability: Return-Or-Refund.Initiate
    Stub: initiates a return/refund flow.
    """

    payload = envelope.get("payload", {})
    item = payload.get("item")
    reason = payload.get("reason")

    return {
        "message": "Stub return/refund initiated.",
        "item": item,
        "reason": reason,
        "status": "initiated",
        "correlationId": envelope.get("correlationId"),
    }
