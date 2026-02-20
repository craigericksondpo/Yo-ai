# agents/rewards_seeker/rewards_profile_request.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    fields = payload.get("fields", [])

    return {
        "message": "Stub rewards profile request.",
        "requestedFields": fields,
        "profile": {},
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
