# agents/ip_inspector/related_ip_discover.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    ip_asset = payload.get("ipAsset")

    return {
        "message": "Stub related IP discovery.",
        "ipAsset": ip_asset,
        "related": [],
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
