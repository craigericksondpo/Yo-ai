# solicitor_general.py - Solicitor-General implementation

from typing import Any, Dict, Optional
import uuid
import time

from core.platform_agent import PlatformAgent
from a2a.registry import AgentRegistry
from core.runtime.schema_loader import SchemaLoader
from app.config import configure_logging
from core.envelopes import AgentContext, CallerInfo, SubjectProfile

log = configure_logging()


class SolicitorGeneral(PlatformAgent):
    """
    MVP Solicitor-General:
    - Accepts A2A requests
    - Looks up target capability/agent
    - Invokes agent
    - Maintains a simple correlation map
    - Wraps responses in A2AResponse shape
    - Relies on ErrorsMiddleware for uncaught exceptions
    """

    lifespan = "persistent"

    def __init__(self, agent_id: str = "solicitor_general"):
        super().__init__(agent_id)
        self.correlation_map: Dict[str, Dict[str, Any]] = {}
        self.knowledge = self.load_knowledge()
        
        # Optional: load A2A schemas if you want validation later
        self.a2a_request_schema = SchemaLoader.load("yo_ai_main/a2a/schemas/a2a-request.schema.json")
        self.a2a_response_schema = SchemaLoader.load("yo_ai_main/a2a/schemas/a2a-response.schema.json")

    # ------------------------------------------------------------------
    # Public entrypoint: handle an A2A request (already JSON-decoded)
    # ------------------------------------------------------------------
    async def handle_a2a(self, request: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        request: A2ARequest-like dict with at least:
          - method
          - params
          - id (JSON-RPC id)
        context: optional dict with correlationId, principalId, trustTier, etc.
        """
        context = context or {}
        correlation_id = context.get("correlationId") or str(uuid.uuid4())
        method = request.get("method")
        rpc_id = request.get("id")

        start = time.time()

        log.info(
            "sg.request.received",
            extra={
                "correlationId": correlation_id,
                "method": method,
                "rpcId": rpc_id,
            },
        )

        # Dispatch based on method
        if method == "send_message":
            result = await self._handle_send_message(request, correlation_id, context)
        elif method == "get_task":
            result = await self._handle_get_task(request, correlation_id, context)
        else:
            # MVP: unsupported methods return JSON-RPC error
            return self._wrap_error_response(
                rpc_id=rpc_id,
                correlation_id=correlation_id,
                code=-32601,
                message=f"Method not supported by SG MVP: {method}",
            )

        duration_ms = (time.time() - start) * 1000.0

        log.info(
            "sg.request.completed",
            extra={
                "correlationId": correlation_id,
                "method": method,
                "rpcId": rpc_id,
                "latencyMs": duration_ms,
            },
        )

        return result

    # ------------------------------------------------------------------
    # send_message → route to target agent + capability
    # ------------------------------------------------------------------
    async def _handle_send_message(
        self,
        request: Dict[str, Any],
        correlation_id: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        rpc_id = request.get("id")
        params = request.get("params", {})

        # MVP assumption: params contain target_agent_id and capability
        target_agent_id = params.get("target_agent_id")
        capability = params.get("capability")
        payload = params.get("payload", {})

        if not target_agent_id or not capability:
            return self._wrap_error_response(
                rpc_id=rpc_id,
                correlation_id=correlation_id,
                code=-32602,
                message="Missing target_agent_id or capability in params",
            )

        agent = AgentRegistry.get(target_agent_id)
        if agent is None:
            return self._wrap_error_response(
                rpc_id=rpc_id,
                correlation_id=correlation_id,
                code=-32004,
                message=f"Unknown agent: {target_agent_id}",
            )

        # Record correlation (MVP: one entry per RPC id)
        self.correlation_map[rpc_id] = {
            "correlationId": correlation_id,
            "targetAgentId": target_agent_id,
            "capability": capability,
        }

        log.info(
            "sg.routing.decision",
            extra={
                "correlationId": correlation_id,
                "rpcId": rpc_id,
                "targetAgentId": target_agent_id,
                "capability": capability,
            },
        )

        # MVP: assume agent has a generic handle_capability method
        result = await agent.handle_capability(
            capability=capability,
            payload=payload,
            context={
                "correlationId": correlation_id,
                "principalId": context.get("principalId"),
                "trustTier": context.get("trustTier"),
            },
        )

        # Wrap as A2AResponse
        return self._wrap_success_response(
            rpc_id=rpc_id,
            correlation_id=correlation_id,
            method="send_message",
            result=result,
        )

    # ------------------------------------------------------------------
    # get_task → simple lookup in correlation map (MVP)
    # ------------------------------------------------------------------
    async def _handle_get_task(
        self,
        request: Dict[str, Any],
        correlation_id: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        rpc_id = request.get("id")
        params = request.get("params", {})
        task_id = params.get("task_id")

        if not task_id:
            return self._wrap_error_response(
                rpc_id=rpc_id,
                correlation_id=correlation_id,
                code=-32602,
                message="Missing task_id in params",
            )

        # MVP: just echo back a stub; real implementation will query SG task registry
        task_info = {
            "task_id": task_id,
            "status": "completed",
            "result": None,
        }

        log.info(
            "sg.task.lookup",
            extra={
                "correlationId": correlation_id,
                "rpcId": rpc_id,
                "taskId": task_id,
            },
        )

        return self._wrap_success_response(
            rpc_id=rpc_id,
            correlation_id=correlation_id,
            method="get_task",
            result=task_info,
        )

    # ------------------------------------------------------------------
    # Response wrapping (JSON-RPC style)
    # ------------------------------------------------------------------
    def _wrap_success_response(
        self,
        rpc_id: Any,
        correlation_id: str,
        method: str,
        result: Any,
    ) -> Dict[str, Any]:
        response = {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "method": method,
            "result": result,
        }

        log.info(
            "sg.response.success",
            extra={
                "correlationId": correlation_id,
                "rpcId": rpc_id,
                "method": method,
            },
        )

        return response

    def _wrap_error_response(
        self,
        rpc_id: Any,
        correlation_id: str,
        code: int,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        error_obj: Dict[str, Any] = {
            "code": code,
            "message": message,
        }
        if data is not None:
            error_obj["data"] = data

        response = {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": error_obj,
        }

        log.error(
            "sg.response.error",
            extra={
                "correlationId": correlation_id,
                "rpcId": rpc_id,
                "errorCode": code,
                "errorMessage": message,
            },
        )

        return response


    # ------------------------------------------------------------------
    # sets AgentContext in the envelope when routing to target agent
    # ------------------------------------------------------------------

    def build_context(self, envelope: dict) -> AgentContext:
        caller = CallerInfo(
            id=envelope["caller"]["id"],
            type=envelope["caller"].get("type", "unknown"),
            metadata=envelope["caller"].get("metadata", {})
        )

        subject = SubjectProfile(
            id=envelope["subject"]["id"],
            attributes=envelope["subject"].get("attributes", {})
        )

        profile = envelope.get("profile", {})

        return AgentContext(
            caller=caller,
            subject=subject,
            profile=profile,
            correlation_id=envelope.get("correlationId", ""),
            raw_envelope=envelope
        )
    


    async def handle_capability(self, capability: str, payload: dict, context: dict):
        if capability == "Just-Ask":
            return self._just_ask()

        return {"message": f"Unknown SG capability: {capability}"}


    def _just_ask(self):
        return {
            "introduction": (
                "Welcome to the Yo-ai Platform. I am the Solicitor-General, the "
                "coordination and governance agent responsible for routing, "
                "correlation, negotiation, and task lifecycle management across "
                "all agents in this ecosystem."
            ),
            "what_you_can_do": [
                "Announce your intent",
                "Request a capability (e.g., Data-Steward.Normalize)",
                "Ask which agents are available",
                "Begin or resume a task",
                "Explore platform conventions",
            ],
            "next_steps": (
                "State your intent or request a capability and I will assist you."
            ),
        }