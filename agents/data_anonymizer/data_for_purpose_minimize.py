# agents/data_anonymizer/data_for_purpose_minimize.py

async def run(envelope, context):
    payload = envelope.get("payload", {})
    purpose = payload.get("purpose")
    fields = payload.get("fields", [])

    return {
        "message": "Stub data minimization.",
        "purpose": purpose,
        "requiredFields": fields[:2],
        "unnecessaryFields": fields[2:],
        "correlationId": envelope.get("correlationId"),
    }
