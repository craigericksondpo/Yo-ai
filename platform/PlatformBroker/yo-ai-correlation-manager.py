# 2. Pruning daemon that uses the cleanup function:	periodic_cleanup_and_mark_orphans 
# to assign correlation IDs and mark orphans and expired request-response pairs (including tasks).
# A simple daemon loop runs on a schedule and emits Kafka events when correlation is assigned
#  and when an A2A request/response or task is marked expired/orphaned.
Extended cleanup function
import uuid
import time
from datetime import datetime, timedelta

def generate_correlation_id():
    return f"corr-{uuid.uuid4()}"

def periodic_cleanup_and_mark_orphans(storage, kafka_producer, ttl_minutes=30):
    """
    - Assigns correlation IDs for long-running or expired tasks.
    - Marks expired tasks as 'expired' if not resolved.
    - Emits Kafka events for correlation assignment and expiration.
    """

    now = datetime.utcnow()
    ttl = timedelta(minutes=ttl_minutes)

    active_tasks = storage.list_tasks(status="pending")
    checked = 0
    correlated = 0
    expired = 0

    for task in active_tasks:
        checked += 1

        created_at = task.get("createdAt")
        is_long_running = task.get("longRunning", False)
        correlation_id = task.get("correlationId")
        status = task.get("status", "pending")

        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        ttl_expired = (now - created_at) > ttl

        # 1. Assign correlationId if long-running or TTL expired and none exists
        if (is_long_running or ttl_expired) and not correlation_id:
            correlation_id = generate_correlation_id()
            correlated += 1

            storage.update_task(
                task_id=task["id"],
                correlationId=correlation_id,
                correlationAssignedAt=now.isoformat(),
                correlationReason="long_running" if is_long_running else "ttl_expired"
            )

            # Emit correlation assignment event
            event = {
                "eventType": "CORRELATION_ASSIGNED",
                "eventVersion": "1.0.0",
                "emittedAt": now.isoformat() + "Z",
                "taskId": task["id"],
                "correlationId": correlation_id,
                "correlationReason": "long_running" if is_long_running else "ttl_expired",
                "correlationAssignedAt": now.isoformat() + "Z",
                "longRunning": is_long_running,
                "ttlExpired": ttl_expired,
                "requestPresent": bool(task.get("request")),
                "responsePresent": bool(task.get("response")),
                "requestJsonRpcId": (task.get("request") or {}).get("id"),
                "responseJsonRpcId": (task.get("response") or {}).get("id"),
                "tags": {
                    "service": "solicitor-general",
                    "environment": "prod"
                }
            }
            kafka_producer.send("a2a.correlation-assigned.v1", event)

        # 2. Normalize correlation across request/response
        request = task.get("request") or {}
        response = task.get("response") or {}

        req_corr = request.get("correlationId")
        res_corr = response.get("correlationId")

        # (a) If we just generated tak-level correlationId, propagate it
        if correlation_id:
            if request and not req_corr:
                request = {**request, "correlationId": correlation_id}
            if response and not res_corr:
                response = {**response, "correlationId": correlation_id}

        # (b) If only one side has corr, propagate to the other
        if req_corr and not res_corr:
            response = {**response, "correlationId": req_corr}
        elif res_corr and not req_corr:
            request = {**request, "correlationId": res_corr}

        # If changed, persist
        storage.update_task(
            task_id=task["id"],
            request=request if request else None,
            response=response if response else None,
        )

        # 3. Mark expired/orphaned (no response) but keep for audit
        if ttl_expired and status == "pending":
            # Define "orphaned" as: request present but no response
            has_request = bool(request)
            has_response = bool(response)

            if has_request and not has_response:
                new_status = "orphaned"
            else:
                new_status = "expired"

            expired += 1

            storage.update_task(
                task_id=task["id"],
                status=new_status,
                finalizedAt=now.isoformat(),
            )

            event = {
                "eventType": "TASK_EXPIRED",
                "eventVersion": "1.0.0",
                "emittedAt": now.isoformat() + "Z",
                "taskId": task["id"],
                "status": new_status,
                "ttlExpired": ttl_expired,
                "longRunning": is_long_running,
                "correlationId": correlation_id,
                "tags": {
                    "service": "solicitor-general",
                    "environment": "prod"
                }
            }
            kafka_producer.send("a2a.task-lifecycle.v1", event)

    return {
        "status": "ok",
        "checked": checked,
        "correlated": correlated,
        "expired": expired
    }

# Simple pruning daemon loop
# You can run this in a dedicated process, container, or as a background thread.
# You can easily swap:
# •	print → structured logging
# •	hard-coded topics → config/env vars
# •	interval_seconds and ttl_minutes → per-tenant overrides, etc.


def pruning_daemon(storage, kafka_producer, ttl_minutes=30, interval_seconds=60):
    """
    Simple long-running daemon that periodically runs cleanup.
    """

    while True:
        started_at = datetime.utcnow()
        result = periodic_cleanup_and_mark_orphans(
            storage=storage,
            kafka_producer=kafka_producer,
            ttl_minutes=ttl_minutes
        )
        finished_at = datetime.utcnow()

        print(
            f"[{finished_at.isoformat()}] Cleanup run: "
            f"checked={result['checked']} "
            f"correlated={result['correlated']} "
            f"expired={result['expired']} "
            f"duration={(finished_at - started_at).total_seconds():.3f}s"
        )

        time.sleep(interval_seconds)
