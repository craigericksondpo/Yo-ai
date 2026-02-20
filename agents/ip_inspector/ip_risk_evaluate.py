# agents/ip_inspector/ip_risk_evaluate.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    ip_asset = payload.get("ipAsset")

    return {
        "message": "Stub IP risk evaluation.",
        "ipAsset": ip_asset,
        "riskScore": 0.0,
        "factors": [],
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
