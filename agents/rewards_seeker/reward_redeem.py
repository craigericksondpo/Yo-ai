# agents/rewards_seeker/reward_redeem.py

import time

async def run(envelope, context):
    payload = envelope.get("payload", {})
    reward_id = payload.get("rewardId")

    return {
        "message": "Stub reward redemption.",
        "rewardId": reward_id,
        "status": "pending",
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
