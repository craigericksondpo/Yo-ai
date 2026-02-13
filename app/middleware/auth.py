# auth.py - request auth
# yo_ai_main/app/middleware/auth.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from yo_ai_main.app.config import configure_logging

log = configure_logging()


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Door-Keeper (MVP):
    - Establishes principalId, authSource, trustTier
    - For now, treats everything as internal/trusted
    - Attaches identity to request.state for SG and agents
    """

    async def dispatch(self, request: Request, call_next):
        # MVP: hard-coded internal principal
        principal_id = request.headers.get("x-principal-id", "internal")
        auth_source = request.headers.get("x-auth-source", "internal")
        trust_tier = request.headers.get("x-trust-tier", "internal")

        request.state.principal_id = principal_id
        request.state.auth_source = auth_source
        request.state.trust_tier = trust_tier

        log.info(
            "auth.context",
            extra={
                "correlationId": getattr(request.state, "correlation_id", None),
                "principalId": principal_id,
                "authSource": auth_source,
                "trustTier": trust_tier,
            },
        )

        response: Response = await call_next(request)
        return response