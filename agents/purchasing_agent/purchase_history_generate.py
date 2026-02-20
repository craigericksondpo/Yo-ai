# agents/purchasing_agent/purchase_history_generate.py

async def run(envelope, context):
    """
    Capability: Purchase-History.Generate
    Stub: returns a fake purchase history.
    """

    return {
        "message": "Stub purchase history generated.",
        "history": [
            {"item": "Example Item A", "price": 19.99, "timestamp": "2026-01-01"},
            {"item": "Example Item B", "price": 42.00, "timestamp": "2026-01-15"},
        ],
        "correlationId": envelope.get("correlationId"),
    }
