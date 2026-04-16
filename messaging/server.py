from typing import Any
from websockets import serve, ServerConnection, broadcast, ConnectionClosed
from json import dumps, loads

import asyncio


class ConnectedClient:
    def __init__(self, connection: ServerConnection, username: str) -> None:
        self.connection = connection
        self.username = username


connected_clients: list[ConnectedClient] = []


def broadcast_json(recipients: list[ServerConnection], data: Any):
    broadcast(recipients, dumps(data))


async def on_client_connect(client_ws: ServerConnection):
    username = await client_ws.recv()

    if not isinstance(username, str):
        return

    client = ConnectedClient(client_ws, username)

    connected_clients.append(client)

    broadcast_json(
        [other.connection for other in connected_clients if other != client],
        {"type": "member_online", "data": {"name": username}},
    )

    try:
        while True:
            message = str(await client_ws.recv())

            broadcast_json(
                [other.connection for other in connected_clients if other != client],
                {
                    "type": "message",
                    "data": {"content": message, "sender": client.username},
                },
            )
    except ConnectionClosed:
        pass
    finally:
        broadcast_json(
            [other.connection for other in connected_clients if other != client],
            {"type": "member_offline", "data": {"name": username}},
        )
        connected_clients.remove(client)


async def main():
    host = input("host: ")
    port = int(input("port: "))

    async with serve(on_client_connect, host=host, port=port) as server:
        print(f"hosting room @ ws://{host}:{port}")
        await server.serve_forever()


asyncio.run(main())
