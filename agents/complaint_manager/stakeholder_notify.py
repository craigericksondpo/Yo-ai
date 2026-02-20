# agents/complaint_manager/stakeholder_notify.py

import time


async def run(envelope, context):
    """
    Capability: Stakeholder.Notify

    Stub: sends a notification to a stakeholder.
    """

    payload = envelope.get("payload", {})
    stakeholder = payload.get("stakeholder")
    complaint_id = payload.get("complaintId")

    return {
        "message": "Stub stakeholder notification.",
        "stakeholder": stakeholder,
        "complaintId": complaint_id,
        "status": "notified",
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
