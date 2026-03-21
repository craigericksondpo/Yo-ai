# shared/tools/tool_invocation_manager.py
#
# Async tool dispatcher — the agent-facing API for tool invocation.
#
# Sits above ToolRegistry. Adds:
#   - LOGGING.md tool boundary pattern (pre-call + post-call audit log entries)
#   - ToolResult inspection and structured error reporting
#   - dry_run support — skips actual invocation when capability_ctx.dry_run
#   - Per-invocation correlation ID and task ID in every log entry
#
# Gap Registry v2 fixes:
#   - No error handling around tool execution → all errors now caught and
#     returned as ToolResult. Raw ValueError/exceptions no longer escape.
#   - Tool system redesign: reads from x-artifacts (via bootstrap_tools),
#     not x-tools (dead path).
#
# Usage in run() modules:
#
#   from shared.tools.tool_invocation_manager import ToolInvocationManager
#
#   tim = ToolInvocationManager(registry=agent.tool_registry)
#
#   result = await tim.invoke(
#       tool_name="AccessAdministrator",
#       payload={"action": "grant", "subjectId": subject_id},
#       agent_ctx=agent_ctx,
#       capability_ctx=capability_ctx,
#   )
#
#   if not result.success:
#       # handle error — result.error describes what went wrong
#       ...

import logging
from typing import Any

from shared.tools.tool_registry import ToolRegistry, ToolResult

logger = logging.getLogger(__name__)


class ToolInvocationManager:
    """
    Agent-facing API for tool invocation.

    Wraps ToolRegistry.invoke() with:
      - LOGGING.md tool boundary pattern (pre-call + post-call audit entries)
      - dry_run support
      - structured ToolResult returns — never raises

    Instantiated per-agent, injected with the agent's ToolRegistry.
    """

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    async def invoke(
        self,
        tool_name: str,
        payload: dict,
        agent_ctx: Any,
        capability_ctx: Any,
    ) -> ToolResult:
        """
        Invoke a tool and return a ToolResult.

        Implements the LOGGING.md tool boundary pattern:
          1. Log pre-call entry (with correlationId + taskId)
          2. Skip actual call if dry_run=True
          3. Invoke tool
          4. Log post-call entry (with correlationId + taskId + outcome)

        Args:
            tool_name      : Name of the registered tool (e.g. "AccessAdministrator")
            payload        : Tool input payload dict
            agent_ctx      : AgentContext — provides correlation_id, task_id, log()
            capability_ctx : CapabilityContext — provides dry_run flag

        Returns:
            ToolResult — always. Never raises.
        """
        correlation_id = agent_ctx.correlation_id
        task_id        = agent_ctx.task_id
        dry_run        = capability_ctx.dry_run

        # ------------------------------------------------------------------
        # 1. Pre-call audit log entry (LOGGING.md tool boundary pattern)
        # ------------------------------------------------------------------
        agent_ctx.log(
            event_type=f"{tool_name}.Call",
            message=f"Tool invocation — pre-call audit bridge.",
            data={
                "tool":          tool_name,
                "action":        payload.get("action"),
                "dryRun":        dry_run,
                "correlationId": correlation_id,
                "taskId":        task_id,
                # payload fields safe to log — no credential material
                # full payload intentionally excluded
            }
        )

        # ------------------------------------------------------------------
        # 2. dry_run: skip actual invocation
        # ------------------------------------------------------------------
        if dry_run:
            result = ToolResult.ok(
                tool_name=tool_name,
                output={"dryRun": True, "message": f"Tool '{tool_name}' skipped — dry_run=True."},
            )
            self._log_post_call(agent_ctx, tool_name, result, dry_run=True)
            return result

        # ------------------------------------------------------------------
        # 3. Invoke — ToolRegistry catches all exceptions internally
        # ------------------------------------------------------------------
        try:
            result = await self.registry.invoke(
                name=tool_name,
                payload=payload,
                context={
                    "correlationId": correlation_id,
                    "taskId":        task_id,
                },
            )
        except Exception as exc:
            # Should never reach here — ToolRegistry.invoke() never raises.
            # This is a last-resort safety net.
            logger.error(
                "ToolInvocationManager: unexpected exception from "
                "registry.invoke('%s') — %s", tool_name, exc
            )
            result = ToolResult.execution_error(tool_name, exc)

        # ------------------------------------------------------------------
        # 4. Post-call audit log entry (LOGGING.md tool boundary pattern)
        # ------------------------------------------------------------------
        self._log_post_call(agent_ctx, tool_name, result, dry_run=False)

        return result

    def _log_post_call(
        self,
        agent_ctx: Any,
        tool_name: str,
        result: ToolResult,
        dry_run: bool,
    ) -> None:
        """Write the post-call audit log entry."""
        agent_ctx.log(
            event_type=f"{tool_name}.Return",
            message=f"Tool invocation — post-call audit bridge.",
            data={
                "tool":          tool_name,
                "success":       result.success,
                "errorType":     result.error_type,
                "error":         result.error,
                "dryRun":        dry_run,
                "correlationId": agent_ctx.correlation_id,
                "taskId":        agent_ctx.task_id,
                # output intentionally excluded — log shape/outcome only,
                # never raw tool output (may contain personal data)
            }
        )
