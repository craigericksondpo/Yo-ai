# errors.py - exception handlers
# yo_ai_main/app/middleware/errors.py

import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from yo_ai_main.app.config import configure_logging

log = configure_logging()


class ErrorsMiddleware(BaseHTTPMiddleware):
    """
    Incident-Responder (MVP):
    - Catches uncaught exceptions from downstream
    - Logs a structured error event
    - Returns a safe JSON error response
    """

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            correlation_id = getattr(request.state, "correlation_id", None)
            principal_id = getattr(request.state, "principal_id", None)

            # Structured error log (MVP; later this becomes a canonical envelope)
            log.error(
                "incident.unhandled_exception",
                extra={
                    "correlationId": correlation_id,
                    "principalId": principal_id,
                    "errorType": type(exc).__name__,
                    "errorMessage": str(exc),
                    "stackTrace": traceback.format_exc(),
                },
            )

            # Safe error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": type(exc).__name__,
                        "message": "An internal error occurred.",
                        "correlationId": correlation_id,
                    }
                },
            )