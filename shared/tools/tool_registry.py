# shared/tools/tool_registry.py

from typing import Dict, Protocol, Any


class ToolAdapter(Protocol):
    async def execute(self, payload: dict, context: dict) -> dict:
        ...


class ToolRegistry:
    """
    Shared registry for all tool adapters.
    Agents use this to invoke tools by name.
    """

    def __init__(self):
        self._adapters: Dict[str, ToolAdapter] = {}

    def register(self, name: str, adapter: ToolAdapter):
        if name in self._adapters:
            raise ValueError(f"Tool already registered: {name}")
        self._adapters[name] = adapter

    def get(self, name: str) -> ToolAdapter:
        adapter = self._adapters.get(name)
        if not adapter:
            raise ValueError(f"Tool not found: {name}")
        return adapter

    async def invoke(self, name: str, payload: dict, context: dict) -> dict:
        adapter = self.get(name)
        return await adapter.execute(payload, context)
