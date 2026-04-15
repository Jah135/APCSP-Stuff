import asyncio
from websockets import connect


async def main():
    async with connect("ws://localhost:8784") as ws:
        print(await ws.recv())


asyncio.run(main())
