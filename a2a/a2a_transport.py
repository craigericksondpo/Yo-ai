# /a2a/a2a_transport.py

from datetime import datetime

class A2ATransport:
    """
    Protocol-only A2A transport.

    - Accepts raw JSON-RPC envelope
    - Runs mandatory-but-non-blocking validation
    - Extracts request_id (correlation_id)
    - Hands off to the Solicitor-General (semantic boundary)
    - Wraps the result in a JSON-RPC response envelope
    """

    def __init__(self, solicitor_general, logger, validator):
        self._sg = solicitor_general
        self._logger = logger
        self._validator = validator

    async def handle_a2a(self, envelope: dict) -> dict:
        # 0. Extract request_id once at the protocol boundary
        request_id = envelope.get("id")

        # 1. Mandatory-but-non-blocking validation
        validation_info = self._run_validation(envelope)
        self._logger.info("a2a.validation", extra={
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "validation": validation_info,
        })

        # 2. If request_id is missing, do NOT call SG; return a JSON-RPC error with id = null
        if request_id is None:
            self._logger.error("a2a.missing_request_id", extra={
                "timestamp": datetime.utcnow().isoformat(),
                "envelope": envelope,
            })
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": "Missing request_id (JSON-RPC id)",
                },
                "id": None,
            }

        # 3. Hand off to SG (semantic boundary) with a required request_id
        try:
            semantic_result = await self._sg.route(envelope, request_id=request_id)
        except Exception as e:
            self._logger.error("a2a.transport_error", extra={
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": request_id,
                "error": str(e),
                "envelope": envelope,
            })
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)},
                "id": request_id,
            }

        # 4. Wrap in JSON-RPC response
        return {
            "jsonrpc": "2.0",
            "result": semantic_result,
            "id": request_id,
        }

    def _run_validation(self, envelope: dict) -> dict:
        """
        Mandatory-but-non-blocking validation against A2A versions.
        Never raises; always returns a structured info object.
        """
        info = {"v1_0_valid": False, "v0_3_valid": False, "errors": []}

        try:
            info["v1_0_valid"] = self._validator.validate_v1(envelope)
        except Exception:
            pass

        try:
            info["v0_3_valid"] = self._validator.validate_v03(envelope)
        except Exception:
            pass

        if not info["v1_0_valid"] and not info["v0_3_valid"]:
            try:
                info["errors"] = (
                    self._validator.errors_v1(envelope)
                    + self._validator.errors_v03(envelope)
                )
            except Exception:
                info["errors"] = ["validation failed unexpectedly"]

        return info
