import asyncio
from websockets import serve


async def on_connection(ws):
    print(ws)


async def main():
    async with serve(on_connection, "localhost", 8784) as server:
        await server.serve_forever()


asyncio.run(main())
