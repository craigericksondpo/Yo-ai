# a2a/handlers.py - request/response/event handlers

# THIS IS NOT the entry point for Yo-ai. 
# It is for app.py which uses Starlette to route HTTP requests to these handlers. 
# These handlers delegate to the FastA2AApp instance (a2a_app) which implements the A2A protocol logic.
# Yo-ai does not use Starlette OR FastA2A any longer. This is only an option for other developers.

from starlette.responses import JSONResponse
from starlette.requests import Request

from .app import a2a_app


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

