# agents/complaint_manager/stakeholders_get.py

import time


async def run(envelope, context):
    """
    Capability: Stakeholders.Get

    Stub: retrieves stakeholders relevant to the complaint.
    """

    payload = envelope.get("payload", {})
    org = payload.get("organization")

    return {
        "message": "Stub stakeholder retrieval.",
        "organization": org,
        "stakeholders": ["StubStakeholderA", "StubStakeholderB"],
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
