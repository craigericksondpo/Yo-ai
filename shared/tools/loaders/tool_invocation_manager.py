# shared/tools/loaders/tool_invocation_manager.py

from importlib import import_module

class ToolInvocationManager:
    def __init__(self, adapters: dict[str, object]):
        self.adapters = adapters

    async def invoke(self, tool_name: str, payload: dict, context: dict) -> dict:
        adapter = self.adapters.get(tool_name)
        if not adapter:
            raise ValueError(f"No adapter registered for tool: {tool_name}")
        return await adapter.execute(payload, context)
