# shared/tools/adapters/vault_adapter_tool.py

class VaultAdapterTool:
    def __init__(self, vault_adapter):
        self.vault = vault_adapter

    async def execute(self, payload: dict, context: dict) -> dict:
        action = payload.get("action")
        if action == "fetch_fields":
            return await self.vault.fetch_fields(payload["fields"], context)
        if action == "list_inventory":
            return await self.vault.list_inventory()
        raise ValueError(f"Unknown VaultAdapter action: {action}")
