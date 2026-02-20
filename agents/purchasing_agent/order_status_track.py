# agents/purchasing_agent/order_status_track.py

async def run(envelope, context):
    """
    Capability: Order-Status.Track
    Stub: returns a fake order status.
    """

    orderId = envelope.get("payload", {}).get("orderId")

    return {
        "message": "Stub order status.",
        "orderId": orderId,
        "status": "in-transit",
        "eta": "2026-02-21",
        "correlationId": envelope.get("correlationId"),
    }
