# yo_ai_main/app/main.py - Starlette app + FastA2A mounts + Solicitor-General bootstrap
# run it with: uvicorn yo_ai_main.app.main:app --reload


from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

import logfire

from yo_ai_main.a2a.app import a2a_app
from yo_ai_main.a2a.handlers import handle_a2a_request, handle_a2a_response, handle_a2a_event

from yo_ai_main.agents.solicitor_general.sg_agent import SolicitorGeneral
from yo_ai_main.a2a.registry import AgentRegistry
from yo_ai_main.app.config import configure_logging

from yo_ai_main.app.routes.root import root
from yo_ai_main.app.routes.a2a import a2a_route


# ------------------------------------------------------------
# 1. Configure logfire (structured logging for Solicitor-General + platform)
# ------------------------------------------------------------
logfire.configure(
    service_name="Solicitor-General",
    level="INFO",
    json_output=True,
)
log = configure_logging()
log.info("Starting Yo-ai Platform runtime")


# ------------------------------------------------------------
# 2. Instantiate the Solicitor-General (PlatformAgent)
# ------------------------------------------------------------
solicitor_general = SolicitorGeneral(
    agent_id="solicitor.general",
    governance_rules={},
    routing_table={}
)

# Register SG with the FastA2A registry
AgentRegistry.register("solicitor.general", solicitor_general)


# ------------------------------------------------------------
# 3. Starlette health endpoints
# ------------------------------------------------------------
async def healthcheck(request):
    return JSONResponse({"status": "ok", "service": "yo-ai-platform"})


# ------------------------------------------------------------
# 4. Starlette app with FastA2A mounts
# ------------------------------------------------------------

routes = [
    Route("/healthz", healthcheck),
    Route("/readyz", healthcheck),

    # A2A protocol endpoints
    Route("/a2a/request", handle_a2a_request, methods=["POST"]),
    Route("/a2a/response", handle_a2a_response, methods=["POST"]),
    Route("/a2a/event", handle_a2a_event, methods=["POST"]),

    # Optional: mount the FastA2A app under /a2a/*
    Mount("/a2a", app=a2a_app),
]

app = Starlette(
    debug=True,
    routes=routes
)

# CHECK: do these already exist in routes?
# app.add_route("/", root, methods=["GET"])
# app.add_route("/a2a", a2a_route, methods=["POST"])

# ------------------------------------------------------------
# 5. Startup hook: loaders, routing, capabilities
# ------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logfire.info("Starting Yo-ai Platform runtime...")

    # Solicitor-General Loaders 
    # solicitor_general.load_knowledge()

    logfire.info("Solicitor-General initialized and ready.")


# ------------------------------------------------------------
# 6. Shutdown hook
# ------------------------------------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    logfire.info("Shutting down Yo-ai Platform runtime...")