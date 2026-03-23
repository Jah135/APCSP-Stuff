from random import choice

with open("data/first_names.txt", "r") as f:
    FIRST_NAMES = [x.strip() for x in f.readlines()]

with open("data/last_names.txt", "r") as f:
    LAST_NAMES = [x.strip() for x in f.readlines()]


def get_first_name() -> str:
    return choice(FIRST_NAMES)


def get_full_name() -> str:
    return f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}"
