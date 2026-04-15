from typing import Any
from wordle import WordleGame
from uuid import UUID
from websockets import serve, ServerConnection
from utils import send_json, recv_json

import asyncio as aio


class ConnectedPlayer:
    def __init__(self, ws: ServerConnection, display_name: str) -> None:
        self.ws = ws
        self.display_name = display_name

    async def notify(self, label: str, data: Any):
        await send_json(self.ws, {"l": label, "d": data})


class OnlineWordleGame(WordleGame):
    def __init__(self) -> None:
        super().__init__()

        self.players: dict[UUID, ConnectedPlayer] = {}

    async def notify_everyone(self, label: str, data: Any):
        for player in self.players.values():
            await player.notify(label, data)

    async def perform_handshake(self, ws: ServerConnection) -> tuple[bool, str]:
        await ws.send("ok_info")

        display_name = str(await ws.recv())

        return True, display_name

    async def on_connection(self, client_ws: ServerConnection):
        ok, display_name = await self.perform_handshake(client_ws)

        if not ok:
            await client_ws.close(405)
            return

        player = ConnectedPlayer(ws=client_ws, display_name=display_name)

        self.players[client_ws.id] = player

        await self.notify_everyone(
            "lobby", [p.display_name for p in self.players.values()]
        )

    async def serve(self, port: int, host: str = "localhost"):
        async with serve(self.on_connection, host=host, port=port) as server:
            print(f"hosting wordle game @ {host}:{port}")
            await server.serve_forever()


async def main():
    game = OnlineWordleGame()
    port = int(input("port: "))

    await game.serve(port=port)


if __name__ == "__main__":
    aio.run(main())
