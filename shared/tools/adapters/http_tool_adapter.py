# shared/tools/adapters/http_tool_adapter.py

import aiohttp

class HttpToolAdapter:
    def __init__(self, url: str):
        self.url = url

    async def execute(self, payload: dict, context: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as resp:
                return await resp.json()

