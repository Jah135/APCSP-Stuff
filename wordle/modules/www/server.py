from typing import Any
from uuid import UUID
from websockets import serve, ServerConnection, ConnectionClosedError, CloseCode
from wordle import get_word_validity

from .utils import broadcast_json, send_json, recv_json

import asyncio


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

        self.guesses: list[str] = []


class WordleServer:
    def __init__(
        self, target_word: str, max_guesses: int = 6, max_players: int = 4
    ) -> None:
        self.connected_players: dict[UUID, ConnectedPlayer] = {}
        self.started = False

        self.target_word = target_word
        self.max_guesses = max_guesses
        self.max_players = max_players

    @property
    def player_count(self) -> int:
        return len(self.connected_players)

    # events

    async def on_player_guess(self, player: ConnectedPlayer, guess: str):
        player.guesses.append(guess)

        await send_json(player.connection, get_word_validity(guess, self.target_word))

    # utility

    async def broadcast_event(self, label: str, data: dict):
        broadcast_json(
            [player.connection for player in self.connected_players.values()],
            {"l": label, "d": data},
        )

    async def run_round(self):
        self.broadcast_event("round_start")

    async def start_game(self):
        if self.started:
            return

        self.started = True

        await self.broadcast_event("display_message", {"message": "Game has started!"})

        while True:
            await self.run_round()

    async def add_player(self, player_ws: ServerConnection, info: dict):
        new_player = ConnectedPlayer(
            player_ws, display_name=info.get("display_name", "MISSING NAME")
        )

        self.connected_players[player_ws.id] = new_player

        await self.broadcast_event(
            "lobby_update",
            {
                "player_list": [
                    player.display_name for player in self.connected_players.values()
                ]
            },
        )

        if self.player_count >= self.max_players:
            asyncio.create_task(self.start_game())

    async def remove_player(self, player_ws: ServerConnection):
        del self.connected_players[player_ws.id]

        await self.broadcast_event(
            "lobby_update",
            {
                "player_list": [
                    player.display_name for player in self.connected_players.values()
                ]
            },
        )

    # procedures

    async def client_event_handler(self, client_ws: ServerConnection):
        player = self.connected_players[client_ws.id]

        while True:
            event: dict = await recv_json(client_ws)
            label: str = event.get("l", "unknown")
            data: dict = event.get("d", {})

            if label == "make_guess":
                await self.on_player_guess(player, data["word"])

    async def perform_handshake(self, client_ws: ServerConnection) -> tuple[bool, dict]:
        await send_json(
            client_ws,
            {
                "l": "lobby_info",
                "d": {"max_guesses": self.max_guesses, "max_players": self.max_players},
            },
        )

        info = await recv_json(client_ws)

        return validate_player_info(info), info

    async def on_client_connect(self, client_ws: ServerConnection):
        if self.started:
            await client_ws.close(CloseCode.NORMAL_CLOSURE, "Game has already started")
            return
        if self.player_count >= self.max_players:
            await client_ws.close(CloseCode.NORMAL_CLOSURE, "Game is full")
            return

        ok, player_info = await self.perform_handshake(client_ws)

        if not ok:
            await client_ws.close()
            print("invalid handshake with connection")
            return

        await self.add_player(client_ws, player_info)

        try:
            await self.client_event_handler(client_ws)
        except ConnectionClosedError:
            pass
        finally:
            print("player disconnected")
            await self.remove_player(client_ws)

    async def serve(self, host: str, port: int):
        async with serve(self.on_client_connect, host=host, port=port) as server:
            print(f"hosting Wordle game at {host}:{port}")
            await server.serve_forever()
