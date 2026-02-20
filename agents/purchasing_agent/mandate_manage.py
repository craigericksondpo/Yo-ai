# agents/purchasing_agent/mandate_manage.py

async def run(envelope, context):
    """
    Capability: Mandate.Manage
    Stub: manages mandates (AP2, recurring payments, etc.)
    """

    mandate = envelope.get("payload", {}).get("mandate")

    return {
        "message": "Stub mandate management.",
        "mandate": mandate,
        "status": "updated",
        "correlationId": envelope.get("correlationId"),
    }
