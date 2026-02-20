# agents/complaint_manager/enforcementagency_get.py

import time


async def run(envelope, context):
    """
    Capability: EnforcementAgency.Get

    Stub: determines the appropriate enforcement agency.
    """

    payload = envelope.get("payload", {})
    mandate = payload.get("mandate")
    jurisdiction = payload.get("jurisdiction")

    return {
        "message": "Stub enforcement agency lookup.",
        "mandate": mandate,
        "jurisdiction": jurisdiction,
        "agency": "StubRegulator",
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
