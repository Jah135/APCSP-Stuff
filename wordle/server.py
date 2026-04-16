from modules.www import WordleServer
import asyncio

new_server = WordleServer("horse", max_players=1)

asyncio.run(new_server.serve("localhost", 6767))
