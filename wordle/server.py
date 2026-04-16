from modules.www import WordleServer
import asyncio

new_server = WordleServer("horse")

asyncio.run(new_server.serve("localhost", 6767))
