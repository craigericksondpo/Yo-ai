# handlers.py - request/response/event handlers

# yo_ai_main/a2a/handlers.py

from starlette.responses import JSONResponse
from starlette.requests import Request

from yo_ai_main.a2a.app import a2a_app


async def handle_a2a_request(request: Request) -> JSONResponse:
    """
    Handles incoming A2A requests (message/send, tasks/get, tasks/cancel, etc.)
    by passing the payload to FastA2AApp.
    """
    payload = await request.json()
    response = await a2a_app.handle_request(payload)
    return JSONResponse(response)


async def handle_a2a_response(request: Request) -> JSONResponse:
    """
    Handles A2A responses sent back to the platform.
    Typically used when an agent responds to a previously submitted task.
    """
    payload = await request.json()
    response = await a2a_app.handle_response(payload)
    return JSONResponse(response)


async def handle_a2a_event(request: Request) -> JSONResponse:
    """
    Handles A2A events (push notifications, streaming updates, etc.)
    """
    payload = await request.json()
    response = await a2a_app.handle_event(payload)
    return JSONResponse(response)

# old version below
# Full A2A HTTP Handler - This is the glue layer between Starlette and FastA2A/Solicitor-General.

from starlette.requests import Request
from starlette.responses import JSONResponse
from yo_ai_main.agents.solicitor_general.sg_agent import SolicitorGeneral

sg = SolicitorGeneral()

async def handle_a2a_http(request: Request):
    """
    HTTP → A2A bridge.
    - Reads JSON body
    - Extracts context from middleware
    - Delegates to SG.handle_a2a
    """
    body = await request.json()

    context = {
        "correlationId": getattr(request.state, "correlation_id", None),
        "principalId": getattr(request.state, "principal_id", None),
        "trustTier": getattr(request.state, "trust_tier", None),
    }

    result = await sg.handle_a2a(body, context)
    return JSONResponse(result)
