# yo_ai_main/app/routes/a2a.py - a2a Route (Starlette)
# This is the public machine facing endpoint that receives A2A JSON RPC requests 
# and hands them to the Solicitor-General.

from starlette.requests import Request
from starlette.responses import JSONResponse
from yo_ai_main.agents.solicitor_general.sg_agent import SolicitorGeneral

sg = SolicitorGeneral()

async def a2a_route(request: Request):
    """
    Unified A2A endpoint.
    - Accepts JSON-RPC A2ARequest
    - Passes it to the Solicitor-General
    - Returns A2AResponse
    """
    body = await request.json()

    context = {
        "correlationId": getattr(request.state, "correlation_id", None),
        "principalId": getattr(request.state, "principal_id", None),
        "trustTier": getattr(request.state, "trust_tier", None),
    }

    response = await sg.handle_a2a(body, context)
    return JSONResponse(response)
