from blessed import Terminal
from websockets import connect, ClientConnection, ConnectionClosed, InvalidURI

from shared import recv_json

import asyncio


term = Terminal()
message_history: list[tuple[str, str]] = []


def on_message_added(content: str, sender: str):
    message_history.append((content, sender))

    with term.location(0, term.height - len(message_history) - 3):
        for content, sender in message_history:
            print(term.clear_eol + f"{sender}: {content}")
            term.move_down()


async def client_event_handler(connection: ClientConnection):
    while True:
        try:
            event: dict = await recv_json(connection)
            event_type: str = event.get("type", "unknown")
            event_data: dict = event.get("data", {})

            if event_type == "member_online":
                on_message_added(
                    f"{event_data["name"]} has entered the room.", "System"
                )
            elif event_type == "member_offline":
                on_message_added(f"{event_data["name"]} has left the room.", "System")
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

            with term.location(y=term.height - 2, x=0):
                print(term.clear_eol + "> " + message_buffer)


async def join_room(room_uri: str, username: str):
    try:
        print(f"connecting to '{room_uri}' as {username}...")
        async with connect(room_uri) as connection:
            await connection.send(username)

            print(term.home + term.clear)

            asyncio.create_task(input_loop(connection))

            await client_event_handler(connection)
    except InvalidURI:
        print("invalid room URI")
    except OSError:
        print(f"unnable to connect to room '{room_uri}'")


async def main():
    username = input("Username: ")
    uri = input("Room URI: ")

    await join_room(uri, username)


asyncio.run(main())
