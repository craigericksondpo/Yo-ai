# agents/complaint_manager/complaint_submit.py

import time


async def run(envelope, context):
    """
    Capability: Complaint.Submit

    Stub: submits a complaint to a regulator or organization.
    """

    payload = envelope.get("payload", {})
    complaint_id = payload.get("complaintId")
    agency = payload.get("agency")

    return {
        "message": "Stub complaint submission.",
        "complaintId": complaint_id,
        "submittedTo": agency,
        "status": "submitted",
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
