import httpx

async def test():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com/user")
        print(r.status_code)

import asyncio
asyncio.run(test())