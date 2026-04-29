from Field import Field, MINE, render_field
from Input import KeyboardInput, PlaybackInput
from random import randint
import keyboard

SEED = randint(0, 19099999)

DO_PLAYBACK = False
DO_RECORD = False

input = KeyboardInput()

if DO_RECORD:
    input.start_recording()

if DO_PLAYBACK:
    print("replaying")

    with open("playback_sequence.txt", "r") as f:
        SEED = int(f.readline())

        input = PlaybackInput([key.strip() for key in f.readlines()], 0.01)

mine_field = Field(30, 30, SEED)
mine_field.place_mines(100)

cursor = (0, 0)


def clamp(value: int, min_val: int, max_val: int):
    return max(min(value, max_val), min_val)


def on_lose():
    print("YOU EXPLODEd!!!!!")


def on_win():
    print("you WINN!!!!!")


def move_cursor(dx: int, dy: int):
    global cursor

    cursor = (
        clamp(cursor[0] + dx, 0, mine_field.width - 1),
        clamp(cursor[1] + dy, 0, mine_field.height - 1),
    )


def redraw_screen():
    print(
        "\x1b[H\x1b[2J"
        + render_field(mine_field, cursor, show_mines=False)
        + f"\n{mine_field.get_flag_count()}/{mine_field.get_state_count(MINE)}\nRECORDING: {DO_RECORD}\nPLAYBACK: {DO_PLAYBACK}"
    )


def on_left_pressed():
    move_cursor(-1, 0)


def on_right_pressed():
    move_cursor(1, 0)


def on_up_pressed():
    move_cursor(0, -1)


def on_down_pressed():
    move_cursor(0, 1)


def on_flag_pressed():
    mine_field.player_flag_cell(*cursor)


def on_dig_pressed():
    mine_field.player_open_cell(*cursor)


KEYMAPPING = {
    "w": on_up_pressed,
    "a": on_left_pressed,
    "s": on_down_pressed,
    "d": on_right_pressed,
    "f": on_flag_pressed,
    "enter": on_dig_pressed,
}

redraw_screen()

while not mine_field.has_exploded:
    key = input.read()

    if key == None:
        continue

    callback = KEYMAPPING.get(key)

    if callback == None:
        continue

    callback()

    redraw_screen()

    if mine_field.is_win_state():
        on_win()
        break
    elif mine_field.has_exploded:
        on_lose()
        break


if DO_RECORD and isinstance(input, KeyboardInput):
    with open("playback_sequence.txt", "w") as f:
        f.write(f"{SEED}\n")
        f.writelines(f"{x}\n" for x in input.stop_recording())

print("press esc to exit.")
keyboard.wait("esc")
