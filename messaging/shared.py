from typing import Any
from websockets.asyncio.connection import Connection
from json import loads, dumps


async def send_json(connection: Connection, data: Any):
    await connection.send(dumps(data))


async def recv_json(connection: Connection):
    return loads(await connection.recv())
