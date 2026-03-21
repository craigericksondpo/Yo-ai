# shared/tools/adapters/http_tool_adapter.py
#
# Fixes applied:
#   - __init__(self, url: str) → __init__(self, *, provider, config)
#     Unified constructor matching bootstrap_tools.py calling convention.
#     url resolved from config["url"] or provider["url"].
#   - New aiohttp.ClientSession() per call — expensive.
#     Session created once at construction and reused.
#     close() added to release the session.
#   - No error handling: HTTP errors, connection failures, JSON decode
#     all propagated raw → all wrapped in try/except, returns structured
#     error dict that ToolRegistry wraps in ToolResult.
#   - No timeout → configurable via config["timeout_seconds"] (default: 30).
#   - auth header injection from config["api_key"] if present.

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30


class HttpToolAdapter:
    """
    Tool adapter for HTTP endpoint tools.

    POSTs the payload as JSON to the configured URL and returns
    the parsed JSON response.

    Constructor (called by bootstrap_tools.py):
        HttpToolAdapter(provider=provider_cfg, config=config_cfg)

    x-artifacts tool entry shape:
        {
          "name": "SomeTool",
          "artifactType": "tool",
          "provider": {
            "name": "HttpTool",
            "url": "https://api.example.com/tool",
            "config": {
              "url": "https://api.example.com/tool",
              "timeout_seconds": 30,
              "api_key_env": "SOME_TOOL_API_KEY"
            }
          }
        }
    """

    def __init__(self, *, provider: dict, config: dict) -> None:
        import os
        # url: prefer config["url"], fall back to provider["url"]
        self.url     = config.get("url") or provider.get("url") or ""
        self.timeout = int(config.get("timeout_seconds", _DEFAULT_TIMEOUT))

        # API key from environment variable (never from card)
        api_key_env  = config.get("api_key_env") or provider.get("api_key_env")
        self.api_key: Optional[str] = os.environ.get(api_key_env) if api_key_env else None

        self._session = None   # created lazily on first execute()

        if not self.url:
            logger.warning(
                "HttpToolAdapter: no url configured — "
                "execute() will fail until url is set."
            )

    async def _get_session(self):
        """Return or create the shared aiohttp session."""
        if self._session is None or self._session.closed:
            import aiohttp
            headers = {}
            if self.api_key:
                headers["x-api-key"] = self.api_key
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    async def execute(self, payload: dict, context: dict) -> dict:
        """
        POST payload to the configured URL and return parsed JSON response.

        Returns a dict. On any failure, returns an error dict rather
        than raising — ToolRegistry wraps this in a ToolResult.
        """
        if not self.url:
            return {
                "success": False,
                "error": "HttpToolAdapter: url not configured.",
            }

        import aiohttp
        try:
            session = await self._get_session()
            timeout = aiohttp.ClientTimeout(total=self.timeout)

            async with session.post(self.url, json=payload, timeout=timeout) as resp:
                if resp.status >= 400:
                    body = await resp.text()
                    return {
                        "success": False,
                        "error": (
                            f"HttpToolAdapter: HTTP {resp.status} from '{self.url}'. "
                            f"body: {body[:200]}"
                        ),
                    }
                return await resp.json()

        except aiohttp.ClientError as exc:
            return {
                "success": False,
                "error": f"HttpToolAdapter: connection error — {exc}",
            }
        except Exception as exc:
            logger.error("HttpToolAdapter: unexpected error — %s", exc)
            return {
                "success": False,
                "error": f"HttpToolAdapter: unexpected error — {exc}",
            }

    async def close(self) -> None:
        """Close the shared aiohttp session. Call during agent teardown."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
