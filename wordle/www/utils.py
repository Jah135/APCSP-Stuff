from typing import Any
from json import loads, dumps
from websockets.asyncio.connection import Connection


async def send_json(ws: Connection, data: Any):
    await ws.send(dumps(data))


async def recv_json(ws: Connection):
    return loads(await ws.recv())
