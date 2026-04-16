from websockets import connect, ClientConnection, ConnectionClosed
from json import loads, dumps

import asyncio


async def client_event_handler(connection: ClientConnection):
    while True:
        try:
            event: dict = loads(await connection.recv())
            event_type: str = event.get("type", "unknown")
            event_data: dict = event.get("data", {})

            if event_type == "member_online":
                print(f"{event_data["name"]} is online.")
            elif event_type == "member_offline":
                print(f"{event_data["name"]} is offline.")
            elif event_type == "message":
                print(f"{event_data["sender"]}: {event_data["content"]}")
        except ConnectionClosed:
            print("connection closed")
            break


async def ainput(prompt: str = ""):
    return await asyncio.to_thread(input, prompt)


async def input_loop(connection: ClientConnection):
    while True:
        content = await ainput()
        await connection.send(content)


async def main():
    username = input("Username: ")
    uri = input("Room URI: ")

    async with connect(uri) as connection:
        await connection.send(username)
        asyncio.create_task(input_loop(connection))
        await client_event_handler(connection)


asyncio.run(main())
