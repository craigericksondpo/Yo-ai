# app/middleware/logging.py

import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from core.runtime.logging.sink_loader import load_log_sink

LOG_SINK = load_log_sink()

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = time.time() - start

        record = {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": int(duration * 1000),
            "timestamp": time.time(),
        }

        try:
            LOG_SINK.write(record)
        except Exception as e:
            # Avoid breaking the request pipeline
            print(f"Logging error: {e}")

        return response
