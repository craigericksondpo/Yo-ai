# agents/purchasing_agent/budget_check.py

async def run(envelope, context):
    """
    Capability: Budget.Check
    Stub: checks available budget.
    """

    budget = 1000  # stubbed

    return {
        "message": "Stub budget check.",
        "availableBudget": budget,
        "correlationId": envelope.get("correlationId"),
    }
