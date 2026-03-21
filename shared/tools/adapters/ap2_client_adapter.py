# shared/tools/adapters/ap2_client_adapter.py
#
# Fixes applied:
#   - __init__(self, binary_path: str) → __init__(self, *, provider, config)
#     Unified constructor matching bootstrap_tools.py calling convention.
#     binary_path resolved from config["binary_path"] or provider["path"].
#   - No timeout on subprocess communication → configurable timeout via
#     config["timeout_seconds"] (default: 30).
#   - No error handling: subprocess failure, non-zero exit, JSON decode
#     errors all propagated raw → all wrapped in try/except, returns
#     structured error dict that ToolRegistry wraps in ToolResult.
#   - stderr now captured and included in error output for diagnostics.

import asyncio
import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30


class AP2ClientAdapter:
    """
    Tool adapter for binary subprocess tools (AP2 client).

    Spawns a subprocess, sends the payload as JSON on stdin,
    reads the response from stdout as JSON.

    Constructor (called by bootstrap_tools.py):
        AP2ClientAdapter(provider=provider_cfg, config=config_cfg)

    x-artifacts tool entry shape:
        {
          "name": "AP2Client",
          "artifactType": "tool",
          "path": "/path/to/ap2_binary",
          "provider": {
            "name": "AP2",
            "config": {
              "binary_path": "/opt/ap2/ap2_client",
              "timeout_seconds": 30
            }
          }
        }
    """

    def __init__(self, *, provider: dict, config: dict) -> None:
        # binary_path: prefer config["binary_path"], fall back to provider["path"]
        self.binary_path = (
            config.get("binary_path")
            or provider.get("path")
            or ""
        )
        self.timeout = int(config.get("timeout_seconds", _DEFAULT_TIMEOUT))

        if not self.binary_path:
            logger.warning(
                "AP2ClientAdapter: no binary_path configured — "
                "execute() will fail until binary_path is set."
            )

    async def execute(self, payload: dict, context: dict) -> dict:
        """
        Send payload to the AP2 binary via stdin, return parsed stdout.

        Returns a dict. On any failure, returns an error dict rather
        than raising — ToolRegistry wraps this in a ToolResult.
        """
        if not self.binary_path:
            return {
                "success": False,
                "error": "AP2ClientAdapter: binary_path not configured.",
            }

        if not os.path.isfile(self.binary_path):
            return {
                "success": False,
                "error": f"AP2ClientAdapter: binary not found at '{self.binary_path}'.",
            }

        try:
            proc = await asyncio.create_subprocess_exec(
                self.binary_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdin_data = json.dumps(payload).encode("utf-8")

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(stdin_data),
                    timeout=self.timeout,
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.communicate()
                return {
                    "success": False,
                    "error": f"AP2ClientAdapter: subprocess timed out after {self.timeout}s.",
                }

            if proc.returncode != 0:
                stderr_text = stderr.decode("utf-8", errors="replace").strip()
                return {
                    "success": False,
                    "error": (
                        f"AP2ClientAdapter: subprocess exited with code {proc.returncode}. "
                        f"stderr: {stderr_text}"
                    ),
                }

            return json.loads(stdout.decode("utf-8"))

        except json.JSONDecodeError as exc:
            return {
                "success": False,
                "error": f"AP2ClientAdapter: failed to parse stdout as JSON — {exc}",
            }
        except Exception as exc:
            logger.error("AP2ClientAdapter: unexpected error — %s", exc)
            return {
                "success": False,
                "error": f"AP2ClientAdapter: unexpected error — {exc}",
            }
