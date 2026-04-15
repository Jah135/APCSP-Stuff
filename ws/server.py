import asyncio
from websockets import serve, ServerConnection


async def on_connection(ws: ServerConnection):
    


async def main():
    async with serve(on_connection, "localhost", 8784) as server:
        await server.serve_forever()


asyncio.run(main())
