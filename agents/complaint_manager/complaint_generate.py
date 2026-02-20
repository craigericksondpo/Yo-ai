# agents/complaint_manager/complaint_generate.py

import time


async def run(envelope, context):
    """
    Capability: Complaint.Generate

    Stub: generates a structured complaint document.
    """

    payload = envelope.get("payload", {})
    findings = payload.get("findings", {})

    return {
        "message": "Stub complaint generation.",
        "findings": findings,
        "complaintDocument": {
            "id": "stub-complaint-123",
            "generatedAt": time.time(),
        },
        "correlationId": envelope.get("correlationId"),
    }
