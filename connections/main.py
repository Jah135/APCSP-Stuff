from random import choice
from typing import TypeVar
import groups
from app import ConnectionsApp

T = TypeVar("T")

def select_random(group: dict[str, T]) -> tuple[str, T]:
	index = choice(list(group.keys()))

	return index, group[index]

print(select_random(groups.HARD))

new_app = ConnectionsApp()
new_app.start()