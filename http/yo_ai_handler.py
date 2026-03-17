# /http/yo_ai_handler.py

"""
Universal Lambda / HTTP entrypoint for the Yo-ai Platform.

This is the front door for ALL agents on the platform. The Solicitor-General
owns the bar — every request enters here regardless of which agent the caller
addressed. Startup Mode 1 (HTTP /a2a POST) and Mode 4 (Starlette/MCP) both
land here.

Module-level singletons are constructed once per Lambda execution environment
and reused across warm invocations. Construction order matters:
  1. PlatformEventBus       — in-process pub/sub for PlatformAgents
  2. capability_map          — loaded from shared/artifacts/capability_map.yaml
  3. SolicitorGeneralAgent   — requires event_bus + capability_map
  4. A2AValidator            — independent, no dependencies
  5. A2ATransport            — requires SG + validator + logger

Capability Map:
  The shared capability map at /shared/artifacts/capability_map.yaml is the
  single source of truth for all platform capabilities and routes. It is
  read/write accessible to all agents. Both this handler and api_handler.py
  load from the same file — no capability paths are hard-coded in either.

Logging:
  A2ATransport uses LogBootstrapper.write(dict) — the platform standard.
  It does NOT use stdlib logger.info() / logger.error().
  The _TransportLoggerAdapter bridges the two interfaces without modifying
  either A2ATransport or LogBootstrapper.
"""

import json
from pathlib import Path

import yaml

from a2a.a2a_transport import A2ATransport
from a2a.a2a_validator import A2AValidator
from agents.solicitor_general.solicitor_general import SolicitorGeneralAgent
from core.platform_agent import PlatformEventBus
from core.runtime.logging.log_bootstrapper import get_logger


# ---------------------------------------------------------------------------
# Transport logger adapter
# ---------------------------------------------------------------------------
# A2ATransport calls self._logger.info(...) and self._logger.error(...) with
# extra= keyword arguments. LogBootstrapper exposes write(dict) only.
# This adapter bridges the two interfaces without modifying either class.

class _TransportLoggerAdapter:
    """
    Adapts LogBootstrapper.write(dict) to the .info() / .error() interface
    that A2ATransport expects. Translates stdlib-style calls into structured
    platform log records.
    """

    def __init__(self, bootstrapper):
        self._log = bootstrapper

    def info(self, event_type: str, extra: dict = None):
        self._log.write({
            "event_type": event_type,
            "level": "INFO",
            "message": event_type,
            "payload": extra or {},
        })

    def error(self, event_type: str, extra: dict = None):
        self._log.write({
            "event_type": event_type,
            "level": "ERROR",
            "message": event_type,
            "payload": extra or {},
        })


# ---------------------------------------------------------------------------
# Shared capability map loader
# ---------------------------------------------------------------------------

def _load_capability_map() -> dict:
    """
    Load the platform capability map from the shared artifacts location:
      /shared/artifacts/capability_map.yaml

    This is the single source of truth for all platform capabilities,
    routes, and constructors. Both yo_ai_handler.py and api_handler.py
    load from this file.

    Returns {} on any failure — the SG will surface Unknown capability
    errors per request rather than crashing on cold start.
    """
    try:
        map_path = (
            Path(__file__).resolve().parent.parent
            / "shared" / "artifacts" / "capability_map.yaml"
        )
        if not map_path.exists():
            print(f"[yo_ai_handler] WARNING: capability_map.yaml not found at {map_path}")
            return {}

        with map_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    except Exception as e:
        print(f"[yo_ai_handler] WARNING: capability_map.yaml failed to load: {e}")
        return {}


# ---------------------------------------------------------------------------
# Module-level singletons
# One set per Lambda execution environment — reused across warm invocations.
# ---------------------------------------------------------------------------

# 1. Platform event bus — in-process pub/sub for PlatformAgents
_event_bus = PlatformEventBus()

# 2. Capability map — single source of truth from shared/artifacts/
_capability_map = _load_capability_map()

# 3. Loggers
_logger_transport_raw = get_logger("transport")
_logger_transport = _TransportLoggerAdapter(_logger_transport_raw)

# 4. Solicitor-General
#    card and extended_card loaded automatically from agent_card/ bundle.
#    capability_map drives all semantic routing decisions.
_sg = SolicitorGeneralAgent(
    event_bus=_event_bus,
    capability_map=_capability_map,
)

# 5. Validator
_validator = A2AValidator()

# 6. Transport
_transport = A2ATransport(
    solicitor_general=_sg,
    logger=_logger_transport,
    validator=_validator,
)


# ---------------------------------------------------------------------------
# Envelope extraction
# ---------------------------------------------------------------------------

def _extract_envelope(event) -> dict | None:
    """
    Extract a JSON-RPC envelope from the inbound event regardless of
    how the Lambda was invoked.

    Handles two shapes:
      - API Gateway Lambda proxy event dict (Mode 1 / Mode 3):
        event is a plain dict with a "body" key containing a JSON string.

      - Direct dict invocation (tests, scripts, Mode 2):
        event is already a well-formed envelope dict (no "body" wrapper).

      - Starlette / FastAPI Request object (Mode 4):
        event has an async .json() method — returns None as sentinel
        for async handling in yo_ai_handler().
    """
    if isinstance(event, dict):
        body = event.get("body")
        if body is not None:
            # API Gateway proxy — body is a JSON string
            try:
                return json.loads(body) if isinstance(body, str) else body
            except json.JSONDecodeError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {e}"},
                }
        # Direct dict — treat as envelope already
        return event

    # Starlette Request or unknown — signal for async handling
    return None


# ---------------------------------------------------------------------------
# Lambda / HTTP entrypoint
# ---------------------------------------------------------------------------

async def yo_ai_handler(event, context=None):
    """
    Universal Lambda / HTTP entrypoint for the Yo-ai Platform.

    Handles all startup modes that arrive at this handler:
      Mode 1 — API Gateway HTTP proxy event (dict with "body" key)
      Mode 4 — Starlette / FastAPI Request object (has async .json())

    For Mode 3 (API Gateway OpenAPI paths), use api_handler.py which wraps
    the request in an A2A-compliant envelope before calling A2ATransport.

    Args:
        event:   API Gateway Lambda proxy event dict, or a Starlette Request.
        context: Lambda context object (optional — not used directly).

    Returns:
        For Lambda proxy (Mode 1): API Gateway response dict with
            statusCode, headers, and JSON body.
        For Starlette (Mode 4): raw response dict from A2ATransport.
    """

    # --- Extract envelope ---
    envelope = _extract_envelope(event)

    if envelope is None:
        # Starlette Request object — async .json() required
        if hasattr(event, "json"):
            try:
                envelope = await event.json()
            except Exception as e:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": f"Parse error: {e}"},
                    }),
                }
        else:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32600, "message": "Unrecognised request format"},
                }),
            }

    # --- Delegate to transport ---
    response = await _transport.handle_a2a(envelope)

    # --- Shape response for Lambda proxy integration ---
    # API Gateway proxy integration expects statusCode + body.
    # Starlette / direct invocation receives the raw response dict.
    if isinstance(event, dict) and "requestContext" in event:
        status_code = 200 if "error" not in response else 400
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response),
        }

    # Starlette / direct — return response dict directly
    return response
