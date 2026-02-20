# agents/purchasing_agent/purchase_risk_evaluate.py

async def run(envelope, context):
    """
    Capability: Purchase-Risk.Evaluate
    Stub: evaluates vendor risk, fraud likelihood, pricing anomalies.
    """

    payload = envelope.get("payload", {})
    vendor = payload.get("vendor")
    item = payload.get("item")
    price = payload.get("price")

    return {
        "message": "Stub risk evaluation from Purchasing-Agent.",
        "vendor": vendor,
        "item": item,
        "price": price,
        "riskScore": 0.25,
        "riskFactors": ["stubbed-risk-factor"],
        "correlationId": envelope.get("correlationId"),
    }
