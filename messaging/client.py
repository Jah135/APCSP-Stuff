from blessed import Terminal
from websockets import connect, ClientConnection, ConnectionClosed, InvalidURI
from math import ceil

from shared import recv_json, send_json, get_local_ip

import asyncio

term = Terminal()
message_history: list[str] = []


def rerender_messages():
    total_lines = sum(
        ceil(len(content) / term.width) + content.count("\n")
        for content in message_history
    )

    print(term.home + term.clear)

    with term.location(0, term.height - 3 - total_lines):
        for message in message_history:
            print(term.clear_eol + message)
            term.move_down()


def on_message_added(content: str):
    message_history.append(content)

    rerender_messages()


async def on_server_event(
    server_ws: ClientConnection, event_type: str, event_data: dict
):
    if event_type == "member_online":
        on_message_added(
            term.green(f"[Server] {event_data["name"]} has entered the room.")
        )
    elif event_type == "member_offline":
        on_message_added(term.red(f"[Server] {event_data["name"]} has left the room."))
    elif event_type == "message":
        on_message_added(f"{event_data["sender"]}: {event_data["content"]}")


async def server_event_handler(server_ws: ClientConnection):
    while True:
        try:
            event: dict = await recv_json(server_ws)

            await on_server_event(
                server_ws, event.get("type", "unknown"), event.get("data", {})
            )

        except ConnectionClosed:
            print("connection closed")
            break


async def post_message(server_ws: ClientConnection, message_content: str):
    await send_json(
        server_ws, {"type": "post_message", "data": {"content": message_content}}
    )


async def input_loop(server_ws: ClientConnection):
    cursor_blink_state = False
    input_buffer = ""

    with term.cbreak(), term.hidden_cursor():
        while True:
            with term.location(y=term.height - 2, x=0):
                print(
                    term.clear_eol
                    + "> "
                    + input_buffer[: term.width - 3]
                    + ("_" if cursor_blink_state else " ")
                )

            key = await term.async_inkey(0.5)

            if key == "":
                cursor_blink_state = not cursor_blink_state

            if not key.is_sequence and key != "":
                input_buffer += key
                cursor_blink_state = False
            else:
                # if key.name == "KEY_LEFT":
                #     cursor_position = max(cursor_position - 1, 0)
                # elif key.name == "KEY_RIGHT":
                #     cursor_position = min(cursor_position + 1, len(input_buffer))
                if key.name == "KEY_BACKSPACE":  # remove
                    if key.modifiers_bits & 4 == 0:
                        input_buffer = ""  # clear it

                    input_buffer = input_buffer[:-1]

                elif key.name == "KEY_ENTER":  # flush & send message
                    await post_message(server_ws, input_buffer)
                    input_buffer = ""
                    cursor_position = 0


async def join_room(room_uri: str, username: str):
    try:
        print(f"connecting to '{room_uri}' as {username}...")
        async with connect(room_uri) as connection:
            await connection.send(username)

            print(term.home + term.clear)

            asyncio.create_task(input_loop(connection))

            await server_event_handler(connection)
    except InvalidURI:
        print("invalid room URI")
    except OSError:
        print(f"unnable to connect to room '{room_uri}'")


async def main():
    username = input("Username: ")
    uri = input("Room URI: ")

    await join_room(uri, username)


asyncio.run(main())
