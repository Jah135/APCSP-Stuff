from typing import Any
from uuid import UUID
from random import choice
from websockets import serve, ServerConnection, ConnectionClosedError

from .utils import broadcast_json, send_json, recv_json
from ..dictionary import DICTIONARY


def validate_player_info(info: Any) -> bool:
    if not isinstance(info, dict):
        return False

    if info.get("display_name") == None:
        return False

    return True


class ConnectedPlayer:
    def __init__(self, connection: ServerConnection, display_name: str) -> None:
        self.connection = connection
        self.display_name = display_name


class WordleServer:
    def __init__(self, target_word: str, max_guesses: int = 6) -> None:
        self.connected_players: dict[UUID, ConnectedPlayer] = {}
        self.target_word = target_word
        self.max_guesses = max_guesses

    async def broadcast_event(self, label: str, data: Any):
        broadcast_json(
            [player.connection for player in self.connected_players.values()],
            {"l": label, "d": data},
        )

    async def add_player(self, player_ws: ServerConnection, info: dict):
        new_player = ConnectedPlayer(
            player_ws, display_name=info.get("display_name", "MISSING NAME")
        )

        self.connected_players[player_ws.id] = new_player

        await self.broadcast_event(
            "lobby_update",
            [player.display_name for player in self.connected_players.values()],
        )

    async def remove_player(self, player_ws: ServerConnection):
        del self.connected_players[player_ws.id]

        await self.broadcast_event(
            "lobby_update",
            [player.display_name for player in self.connected_players.values()],
        )

    async def client_event_handler(self, client_ws: ServerConnection):
        while True:
            event: dict = await recv_json(client_ws)
            label, data = event.get("l"), event.get("d")

            print(label, data)

    async def perform_handshake(self, client_ws: ServerConnection) -> tuple[bool, dict]:
        await send_json(
            client_ws, {"l": "lobby_info", "d": {"max_guesses": self.max_guesses}}
        )

        info = await recv_json(client_ws)

        return validate_player_info(info), info

    async def on_client_connect(self, client_ws: ServerConnection):
        ok, player_info = await self.perform_handshake(client_ws)

        if not ok:
            await client_ws.close()
            print("invalid handshake with connection")
            return

        await self.add_player(client_ws, player_info)

        try:
            await self.client_event_handler(client_ws)
            # await connection.keepalive()
        finally:
            print("player disconnected")
            await self.remove_player(client_ws)

    async def serve(self, host: str, port: int):
        async with serve(self.on_client_connect, host=host, port=port) as server:
            print(f"hosting Wordle game at {host}:{port}")
            await server.serve_forever()
