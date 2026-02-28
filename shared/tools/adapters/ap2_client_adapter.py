# shared/tools/adapters/ap2_client_adapter.py

import asyncio, json

class AP2ClientAdapter:
    def __init__(self, binary_path: str):
        self.binary_path = binary_path

    async def execute(self, payload: dict, context: dict) -> dict:
        proc = await asyncio.create_subprocess_exec(
            self.binary_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate(json.dumps(payload).encode())
        return json.loads(stdout)

