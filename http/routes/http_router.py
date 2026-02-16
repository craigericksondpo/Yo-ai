# http_router.py

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import HTMLResponse, JSONResponse
from starlette.requests import Request

from platform.shared.tools.unified_capability_router import UnifiedCapabilityRouter

semantic_router = UnifiedCapabilityRouter()

# ----------------------------------------------------------------------
# Landing Page
# ----------------------------------------------------------------------

LANDING_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Solicitor-General</title></head>
<body>
    <h1>Solicitor-General A2A Agent</h1>
    <p>This agent routes, logs, and correlates all A2A requests.</p>
    <ul>
        <li><a href="/.well-known/agent-card.json">View Agent Card</a></li>
    </ul>
</body>
</html>
"""

async def landing_page(request: Request):
    return HTMLResponse(LANDING_PAGE)

# ----------------------------------------------------------------------
# Agent Card
# ----------------------------------------------------------------------

AGENT_CARD = {
    "name": "Solicitor-General",
    "version": "1.0.0",
    "description": "Root A2A agent for routing and correlation.",
    "capabilities": [],
    "documentationUrl": "/documentation.md"
}

async def agent_card(request: Request):
    return JSONResponse(AGENT_CARD)

# ----------------------------------------------------------------------
# Identity / Onboarding
# ----------------------------------------------------------------------

async def register(request: Request):
    payload = await request.json()
    return JSONResponse({"status": "registered", "received": payload})

async def auth(request: Request):
    payload = await request.json()
    return JSONResponse({"status": "authenticated", "received": payload})

async def permissions(request: Request):
    payload = await request.json()
    return JSONResponse({"status": "permissions-checked", "received": payload})

async def extended_agent_card(request: Request):
    return JSONResponse({"extended": True, "agent": AGENT_CARD})

# ----------------------------------------------------------------------
# A2A → Semantic Router
# ----------------------------------------------------------------------

async def a2a_entrypoint(request: Request):
    envelope = await request.json()
    result = await semantic_router.route(envelope)
    return JSONResponse(result)

# ----------------------------------------------------------------------
# Starlette App
# ----------------------------------------------------------------------

routes = [
    Route("/", landing_page),
    Route("/.well-known/agent-card.json", agent_card),
    Route("/register", register, methods=["POST"]),
    Route("/auth", auth, methods=["POST"]),
    Route("/permissions", permissions, methods=["POST"]),
    Route("/agent/extended", extended_agent_card),
    Route("/a2a", a2a_entrypoint, methods=["POST"]),

    # Optional mounts
    Mount("/api", app=Starlette(routes=[])),
    Mount("/internal", app=Starlette(routes=[])),
    Mount("/docs", app=Starlette(routes=[])),
]

app = Starlette(debug=False, routes=routes)