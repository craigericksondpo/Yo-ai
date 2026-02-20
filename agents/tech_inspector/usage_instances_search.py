# agents/tech_inspector/usage_instances_search.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    asset = payload.get("asset")

    return {
        "message": "Stub usage instance search.",
        "asset": asset,
        "instances": [],
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
