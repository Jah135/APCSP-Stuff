from wordle import WordlePlayer
from websockets import connect, ClientConnection
from utils import recv_json, send_json

import asyncio as aio


class OnlineWordlePlayer(WordlePlayer):
    def __init__(self, display_name: str) -> None:
        super().__init__()

        self.display_name = display_name

    async def perform_handshake(self, server_ws: ClientConnection) -> bool:
        if await server_ws.recv() != "ok_info":
            return False

        await server_ws.send(self.display_name)

        return True

    async def event_handler(self, server_ws: ClientConnection):
        while True:
            action = await recv_json(server_ws)

            print(action)

    async def connect(self, uri: str):
        async with connect(uri=uri) as ws:
            if not await self.perform_handshake(ws):
                print("invalid handshake")
                await ws.close(405)
                return

            await self.event_handler(ws)


async def main():
    display_name = input("Enter Display Name: ")
    player = OnlineWordlePlayer(display_name)

    uri = "ws://" + input("Enter Server URI: ")
    await player.connect(uri)


if __name__ == "__main__":
    aio.run(main())
