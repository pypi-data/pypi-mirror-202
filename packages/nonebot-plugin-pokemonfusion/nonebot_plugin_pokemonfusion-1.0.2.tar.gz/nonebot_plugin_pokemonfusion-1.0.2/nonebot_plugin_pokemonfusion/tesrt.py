import httpx
import asyncio


async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://raw.githubusercontent.com/Aegide/custom-fusion-sprites/main/CustomBattlers/1.1.png")
        result = resp.content
        print(result)


asyncio.run(main())