# agents/purchasing_agent/purchase_eligibility_validate.py

async def run(envelope, context):
    """
    Capability: Purchase-Eligibility.Validate
    Stub: validates eligibility for purchase.
    """

    payload = envelope.get("payload", {})
    item = payload.get("item")

    return {
        "message": "Stub eligibility validation.",
        "item": item,
        "eligible": True,
        "correlationId": envelope.get("correlationId"),
    }
