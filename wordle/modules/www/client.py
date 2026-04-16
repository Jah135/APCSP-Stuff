from typing import Any
from wordle import WordleGame, LetterValidity
from websockets import connect, ClientConnection

from .utils import recv_json, send_json


def on_lobby_update(new_lobby_list: list[str]):
    print("Lobby List:")
    for player in new_lobby_list:
        print(player)


def on_player_guessed(player: str):
    print(f"{player} has guessed.")


class OnlineWordleGameInterface(WordleGame):
    def __init__(self, display_name: str) -> None:
        super().__init__()

        self.display_name = display_name

    async def make_guess(self, word: str) -> tuple[str, list[LetterValidity]]:  # type: ignore
        connection = self.connection
        await send_json(connection, {"l": "make_guess", "d": {"word": word}})

        guess = (
            word,
            [LetterValidity(validity) for validity in await recv_json(connection)],
        )
        self.guess_history.append(guess)

        return guess

    async def server_event_handler(self):
        server_ws = self.connection

        while True:
            event: dict = await recv_json(server_ws)
            label: str = event.get("l", "unknown")
            data: dict = event.get("d", {})

            if label == "display_message":
                print(data["message"])
            elif label == "lobby_update":
                on_lobby_update(data["player_list"])
            elif label == "player_guessed":
                on_player_guessed(data["player"])
            elif label == "round_start":
                print("round started")

    async def perform_handshake(
        self, server_ws: ClientConnection
    ) -> tuple[bool, dict | None]:
        lobby_event: dict = await recv_json(server_ws)

        if lobby_event.get("l") != "lobby_info":
            return False, None

        lobby_info = lobby_event.get("d")

        if lobby_info == None:
            return False, None

        await send_json(server_ws, {"display_name": self.display_name})

        return True, lobby_info

    async def connect(self, uri: str):
        server_ws = await connect(uri=uri)

        ok, lobby_info = await self.perform_handshake(server_ws)

        if not ok:
            print("invalid handshake")
            await server_ws.close()
            return

        print(lobby_info)

        self.connection = server_ws

        await self.server_event_handler()
