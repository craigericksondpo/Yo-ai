# auth-decorators.py

from functools import wraps
from starlette.responses import JSONResponse

def require_self_or_admin(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        auth = request.scope.get("auth")
        if auth is None:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)

        requested_id = request.path_params.get("user_id")
        authenticated_id = auth.user_id
        roles = auth.roles or []

        if requested_id == authenticated_id or "admin" in roles:
            return await func(request, *args, **kwargs)

        return JSONResponse({"error": "Forbidden"}, status_code=403)

    return wrapper

# Usage:
@require_self_or_admin
async def user_detail(request):
    user_id = request.path_params["user_id"]
    return JSONResponse(get_user_record(user_id))
