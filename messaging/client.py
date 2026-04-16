from blessed import Terminal

from websockets import connect, ClientConnection, ConnectionClosed
from json import loads, dumps

import asyncio


class Message:
    def __init__(self, content: str, sender: str) -> None:
        self.content = content
        self.sender = sender

    @property
    def display(self) -> str:
        return f"{self.sender}: {self.content}"


term = Terminal()
message_history: list[Message] = []


def on_message_added(content: str, sender: str):
    message_history.append(Message(content, sender))

    with term.location(0, term.height - len(message_history) - 3):
        for message in message_history:
            print(term.clear_eol + message.display)
            term.move_down()


async def client_event_handler(connection: ClientConnection):
    while True:
        try:
            event: dict = loads(await connection.recv())
            event_type: str = event.get("type", "unknown")
            event_data: dict = event.get("data", {})

            if event_type == "member_online":
                on_message_added(f"{event_data["name"]} is online.", "System")
            elif event_type == "member_offline":
                on_message_added(f"{event_data["name"]} is offline.", "System")
            elif event_type == "message":
                on_message_added(event_data["content"], event_data["sender"])
        except ConnectionClosed:
            print("connection closed")
            break


async def input_loop(connection: ClientConnection):
    message_buffer = ""

    with term.cbreak(), term.hidden_cursor():
        while True:
            key = await term.async_inkey()

            if not key.is_sequence:
                message_buffer += key
            else:
                if key.name == "KEY_BACKSPACE":  # remove
                    message_buffer = message_buffer[:-1]
                elif key.name == "KEY_ENTER":  # flush
                    await connection.send(message_buffer)

                    message_buffer = ""

            with term.location(y=term.height - 2):
                print(term.clear_bol + term.rjust(message_buffer + " <<"))


async def main():
    username = input("Username: ")
    uri = "ws://localhost:6767"  # input("Room URI: ")

    print(term.home + term.clear)

    async with connect(uri) as connection:
        await connection.send(username)

        asyncio.create_task(input_loop(connection))

        await client_event_handler(connection)


asyncio.run(main())
