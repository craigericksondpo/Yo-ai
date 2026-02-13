# logging.py - logfire middleware
# yo_ai_main/app/middleware/logging.py

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from yo_ai_main.app.config import configure_logging

log = configure_logging()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Outer logging wrapper.
    - Ensures every request has a correlation_id
    - Logs request/response with timing
    - Leaves room to later emit canonical event envelopes
    """

    async def dispatch(self, request: Request, call_next):
        start = time.time()

        # Correlation ID: from header or generated
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        # Attach to scope so downstream (SG, agents) can see it
        request.state.correlation_id = correlation_id

        log.info(
            "http.request",
            extra={
                "correlationId": correlation_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        response: Response = await call_next(request)

        duration_ms = (time.time() - start) * 1000.0

        log.info(
            "http.response",
            extra={
                "correlationId": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "latencyMs": duration_ms,
            },
        )

        # Echo correlation ID back to caller
        response.headers["x-correlation-id"] = correlation_id
        return response