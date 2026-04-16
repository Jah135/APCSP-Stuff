from modules.www import OnlineWordleGame
from websockets import InvalidURI
import asyncio


async def main():
    display_name = input("Enter Display Name: ")
    uri = input("Enter Server URI: ")

    game = OnlineWordleGame(display_name=display_name)

    try:
        await game.connect(uri=uri)
    except InvalidURI as e:
        print(f'Invalid URI "{uri}"\nReason:\n{e}')
    except OSError:
        print(f"Unable to connect to a websocket server at '{uri}'")


asyncio.run(main())
