from pydantic import BaseModel
from typing import Any, Dict

class ToolProvider(BaseModel):
    type: str
    config: Dict[str, Any] = {}

class Tool(BaseModel):
    name: str
    description: str = ""
    capabilities: list[str]
    provider: ToolProvider
    config: Dict[str, Any] = {}

    def execute(self, capability: str, payload: dict):
        raise NotImplementedError("Tool must implement execute()")