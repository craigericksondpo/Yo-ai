# /http/yo_ai_handler.py

from a2a.a2a_transport import A2ATransport
from a2a.a2a_validator import A2AValidator
from agents.solicitor_general.solicitor_general import SolicitorGeneral
from shared.logging import get_logger

# --- module-level singletons (one set per warm Lambda container) ---

_logger_transport = get_logger("transport")
_logger_sg = get_logger("solicitor_general")

_sg = SolicitorGeneral(
    logger=_logger_sg,
)

_validator = A2AValidator()

_transport = A2ATransport(
    solicitor_general=_sg,
    logger=_logger_transport,
    validator=_validator,
)

# --- Lambda/HTTP handler ---

async def yo_ai_handler(request):
    """
    HTTP/Lambda entrypoint.
    Expects a request object with an async .json() method.
    """
    envelope = await request.json()
    response = await _transport.handle_a2a(envelope)
    return response
