# agents/purchasing_agent/budget_after_purchase_update.py

async def run(envelope, context):
    """
    Capability: Budget-After-Purchase.Update
    Stub: updates budget after purchase.
    """

    amount = envelope.get("payload", {}).get("amount")

    return {
        "message": "Stub budget update.",
        "amount": amount,
        "newBudget": 1000 - (amount or 0),
        "correlationId": envelope.get("correlationId"),
    }
