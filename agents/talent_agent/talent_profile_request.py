# agents/talent_agent/talent_profile_request.py

import time


async def run(envelope, context):
    """
    Capability: Talent-Profile.Request

    Stub: requests minimized resume, skills, and professional profile
    from Data-Steward.

    Real implementation would:
      - call Data-Steward → Data-Request.Govern
      - request specific fields
      - return minimized professional profile
    """

    payload = envelope.get("payload", {})
    fields = payload.get("requested_fields", [])

    return {
        "message": "Stub talent profile request.",
        "requestedFields": fields,
        "profile": {},
        "timestamp": time.time(),
        "correlationId": envelope.get("correlationId"),
    }
