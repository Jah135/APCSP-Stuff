from typing import Any, Iterable
from websockets.asyncio.connection import Connection, broadcast
from json import loads, dumps


async def send_json(connection: Connection, data: Any):
    await connection.send(dumps(data))


async def recv_json(connection: Connection):
    return loads(await connection.recv())


def broadcast_json(connections: Iterable[Connection], data: Any):
    broadcast(connections, dumps(data))
