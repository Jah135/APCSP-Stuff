from typing import Any
from json import loads, dumps
from websockets import broadcast
from websockets.asyncio.connection import Connection


def broadcast_json(connections: list[Connection], data: Any):
    broadcast(connections, dumps(data))


async def send_json(connection: Connection, data: Any):
    await connection.send(dumps(data))


async def recv_json(connection: Connection) -> Any:
    return loads(await connection.recv())
