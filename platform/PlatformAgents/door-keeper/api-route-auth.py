# 2. ✔️ Starlette Middleware for Automatic User Scoped Route Enforcement
# api-route-auth.py automatically enforces:
# •	If a route contains {user_id}, it must match the authenticated user
# •	Unless the user has "admin" or a privileged role

# Add to Starlette:
# app.add_middleware(UserScopeMiddleware)
# This gives you automatic enforcement across the entire API surface.


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class UserScopeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        auth = request.scope.get("auth")
        if auth is None:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)

        # Only enforce if the route has a user_id param
        user_id_param = request.path_params.get("user_id")
        if user_id_param is not None:
            if user_id_param != auth.user_id and "admin" not in auth.roles:
                return JSONResponse({"error": "Forbidden"}, status_code=403)

        return await call_next(request)
