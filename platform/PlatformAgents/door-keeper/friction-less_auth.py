from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger("door_keeper")
logger.setLevel(logging.INFO)

class DoorKeeperMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the 'yo-api' header.
    - If header contains a valid Registered Agent Card authToken → trust directly.
    - Otherwise, fall back to Cognito validation.
    """

    def __init__(self, app, storage: Storage, cognito_client=None, kafka_producer=None):
        super().__init__(app)
        self.storage = storage
        self.cognito_client = cognito_client
        self.kafka_producer = kafka_producer

    async def dispatch(self, request, call_next):
        yo_api_key = request.headers.get("yo-api")

        # Log incoming request metadata
        logger.info({
            "event": "incoming_request",
            "path": request.url.path,
            "method": request.method,
            "yo-api": yo_api_key or "MISSING"
        })

        if not yo_api_key:
            return JSONResponse(
                {"error": "Missing yo-api header. Anonymous access only."},
                status_code=401
            )

        # Step 1: Check if yo-api matches a Registered Agent Card in Storage
        registered_card = await self._lookup_registered_card(yo_api_key)
        if registered_card:
            logger.info({"event": "trusted_registered_card", "card": registered_card})
            if self.kafka_producer:
                self.kafka_producer.send("agent-auth", {"status": "trusted", "card": registered_card})
            # Bypass Cognito, allow request
            return await call_next(request)

        # Step 2: Fall back to Cognito validation
        if self.cognito_client:
            try:
                response = self.cognito_client.get_user(AccessToken=yo_api_key)
                logger.info({"event": "cognito_authenticated", "user": response})
                if self.kafka_producer:
                    self.kafka_producer.send("agent-auth", {"status": "cognito", "user": response})
                return await call_next(request)
            except self.cognito_client.exceptions.NotAuthorizedException:
                logger.warning("Invalid yo-api token")
                return JSONResponse({"error": "Invalid yo-api token"}, status_code=403)
            except Exception as e:
                logger.error(f"Cognito validation error: {e}")
                return JSONResponse({"error": "Authentication service unavailable"}, status_code=500)

        # If no Cognito configured, deny
        return JSONResponse({"error": "Authentication required"}, status_code=403)

    async def _lookup_registered_card(self, auth_token: str):
        """
        Query FastA2A Storage for a registered agent card by authToken.
        """
        try:
            # Storage holds tasks; registration tasks include authToken
            tasks = await self.storage.list_tasks(method="agent/register")
            for task in tasks:
                card = task.get("result")
                if card and card.get("authToken") == auth_token:
                    return card
        except Exception as e:
            logger.error(f"Storage lookup failed: {e}")
        return None
