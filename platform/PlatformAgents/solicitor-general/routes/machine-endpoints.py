# 🧪 8. Example Machine Endpoint (Template)
# api/card.py

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from core.decorators import agent_endpoint

router = APIRouter()

@router.get("/card")
@agent_endpoint
async def get_card(request: Request):
    return FileResponse("well-known/agent-card.json")
