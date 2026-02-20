# agents/ip_inspector/ip_assets_discover.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    org = payload.get("organization")

    return {
        "message": "Stub IP asset discovery.",
        "organization": org,
        "assets": [],
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
