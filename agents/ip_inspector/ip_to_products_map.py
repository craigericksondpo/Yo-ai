# agents/ip_inspector/ip_to_products_map.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    ip_asset = payload.get("ipAsset")

    return {
        "message": "Stub IP-to-products mapping.",
        "ipAsset": ip_asset,
        "products": [],
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
