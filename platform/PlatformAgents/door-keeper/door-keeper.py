from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import boto3
import logging

# Configure CloudWatch logging
logger = logging.getLogger("door_keeper")
logger.setLevel(logging.INFO)

# Example Cognito client (adjust region and pool details)
cognito_client = boto3.client("cognito-idp", region_name="us-west-2")

class DoorKeeperMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks the 'yo-api' header against Cognito.
    Logs all traffic to CloudWatch before passing to Solicitor-General.
    """

    async def dispatch(self, request, call_next):
        yo_api_key = request.headers.get("yo-api")

        # Log incoming request metadata
        logger.info({
            "path": request.url.path,
            "method": request.method,
            "headers": dict(request.headers),
            "yo-api": yo_api_key or "MISSING"
        })

        if not yo_api_key:
            # Anonymous pool: limited access
            return JSONResponse(
                {"error": "Missing yo-api header. Anonymous access only."},
                status_code=401
            )

        # Validate against Cognito (stubbed for now)
        try:
            # Example: use Cognito to check token validity
            response = cognito_client.get_user(AccessToken=yo_api_key)
            logger.info({"cognito_user": response})
            # Authenticated pool: allow request
            return await call_next(request)

        except cognito_client.exceptions.NotAuthorizedException:
            logger.warning("Invalid yo-api token")
            return JSONResponse(
                {"error": "Invalid yo-api token"},
                status_code=403
            )
        except Exception as e:
            logger.error(f"Cognito validation error: {e}")
            return JSONResponse(
                {"error": "Authentication service unavailable"},
                status_code=500
            )
