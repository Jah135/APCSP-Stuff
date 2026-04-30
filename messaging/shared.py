# shared.py

from typing import Any, Iterable
from websockets.asyncio.connection import Connection, broadcast
from json import loads, dumps

import socket


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


async def send_json(connection: Connection, data: Any):
    await connection.send(dumps(data))


async def recv_json(connection: Connection):
    return loads(await connection.recv())


def broadcast_json(connections: Iterable[Connection], data: Any):
    broadcast(connections, dumps(data))
