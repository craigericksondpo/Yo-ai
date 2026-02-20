# agents/purchasing_agent/purchase_receipt_generate.py

async def run(envelope, context):
    """
    Capability: Purchase-Receipt.Generate
    Stub: returns a fake AP2-compatible receipt.
    """

    payload = envelope.get("payload", {})
    item = payload.get("item")
    price = payload.get("price")

    return {
        "message": "Stub receipt generated.",
        "receipt": {
            "item": item,
            "price": price,
            "vendor": "StubVendor",
            "timestamp": "2026-02-19T00:00:00Z",
        },
        "correlationId": envelope.get("correlationId"),
    }
