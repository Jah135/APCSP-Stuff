from modules.www import OnlineWordleGameInterface
from websockets import InvalidURI, ConnectionClosedOK
import asyncio


async def main():
    display_name = input("Enter Display Name: ")
    uri = input("Enter Server URI: ")

    game = OnlineWordleGameInterface(display_name=display_name)

    try:
        await game.connect(uri=uri)
    except InvalidURI as e:
        print(f'Invalid URI "{uri}"; {e}')
    except ConnectionClosedOK as e:
        print(f"Server initiated disconnect: {e}")
    except OSError:
        print(f"Unable to connect to a websocket server at '{uri}'")


asyncio.run(main())
