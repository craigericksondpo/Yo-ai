# 🏗️ 2. FastA2A Storage Class Template
# This template gives you:
# •	pluggable backend
# •	audit event emission (Kafka/Logfire)
# •	separate task/context storage
# •	clean async API
# •	ready for your Door Keeper + Solicitor General architecture

from datetime import datetime
from typing import Any, Dict, List, Optional

class Storage:
    """
    FastA2A Storage abstraction.
    Handles:
      - Task Storage (A2A-compliant)
      - Context Storage (agent-specific)
      - Audit event emission
    """

    def __init__(self, backend, audit_emitter=None):
        """
        backend: object implementing get/put/update operations
        audit_emitter: optional Kafka/Logfire emitter
        """
        self.backend = backend
        self.audit = audit_emitter

    # ---------------------------------------------------------
    # TASK STORAGE (A2A-COMPLIANT)
    # ---------------------------------------------------------

    async def create_task(self, task_id: str, initial_status="pending"):
        record = {
            "task_id": task_id,
            "status": initial_status,
            "messages": [],
            "artifacts": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        await self.backend.put(f"task:{task_id}", record)
        self._emit("task.created", record)
        return record

    async def append_message(self, task_id: str, message: Dict[str, Any]):
        record = await self.backend.get(f"task:{task_id}")
        record["messages"].append(message)
        record["updated_at"] = datetime.utcnow().isoformat()
        await self.backend.put(f"task:{task_id}", record)
        self._emit("task.message.appended", {"task_id": task_id, "message": message})

    async def add_artifact(self, task_id: str, artifact: Dict[str, Any]):
        record = await self.backend.get(f"task:{task_id}")
        record["artifacts"].append(artifact)
        record["updated_at"] = datetime.utcnow().isoformat()
        await self.backend.put(f"task:{task_id}", record)
        self._emit("task.artifact.added", {"task_id": task_id, "artifact": artifact})

    async def update_status(self, task_id: str, status: str):
        record = await self.backend.get(f"task:{task_id}")
        record["status"] = status
        record["updated_at"] = datetime.utcnow().isoformat()
        await self.backend.put(f"task:{task_id}", record)
        self._emit("task.status.updated", {"task_id": task_id, "status": status})

    async def get_task(self, task_id: str):
        return await self.backend.get(f"task:{task_id}")

    # ---------------------------------------------------------
    # CONTEXT STORAGE (AGENT-SPECIFIC)
    # ---------------------------------------------------------

    async def save_context(self, task_id: str, agent_type: str, context: Dict[str, Any]):
        record = {
            "task_id": task_id,
            "agent_type": agent_type,
            "context": context,
            "updated_at": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
        await self.backend.put(f"context:{task_id}", record)
        self._emit("context.saved", {"task_id": task_id})
        return record

    async def get_context(self, task_id: str):
        return await self.backend.get(f"context:{task_id}")

    # ---------------------------------------------------------
    # AUDIT EMISSION
    # ---------------------------------------------------------

    def _emit(self, event_type: str, payload: Dict[str, Any]):
        if self.audit:
            self.audit.emit(event_type, payload)
