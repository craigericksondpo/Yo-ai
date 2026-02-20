# agents/purchasing_agent/purchase_initiate.py

async def run(envelope, context):
    """
    Capability: Purchase.Initiate
    Stub: initiates a purchase flow.
    """

    payload = envelope.get("payload", {})
    item = payload.get("item")
    price = payload.get("price")

    return {
        "message": "Stub purchase initiated.",
        "item": item,
        "price": price,
        "status": "pending",
        "correlationId": envelope.get("correlationId"),
    }
