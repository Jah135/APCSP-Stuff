from random import choice
from app import ConnectionsApp
import groups

def select_random(group: dict[str, list[str]]) -> tuple[str, list[str]]:
	index = choice(list(group.keys()))

	return index, group[index]

new_app = ConnectionsApp([
	select_random(groups.EASY),
	select_random(groups.MEDIUM),
	select_random(groups.HARD),
	select_random(groups.TRICKY),
])
new_app.start()