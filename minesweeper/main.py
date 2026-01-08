from Field import Field
from time import sleep
from random import randint
import keyboard

SEED = randint(0, 19099999)

DO_PLAYBACK = False
DO_RECORD = True

current_playback_index = 0
playback_sequence = []

if DO_PLAYBACK:
	print("replaying")

	with open("playback_sequence.txt", "r") as f:
		SEED = int(f.readline())

		playback_sequence = f.readlines()

mine_field = Field(30, 16, SEED)
mine_field.place_mines(70)

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
		clamp(cursor[1] + dy, 0, mine_field.height - 1)
	)
def redraw_screen():
	cursor_index = mine_field.to_index(*cursor)

	print("\x1b[H\x1b[2J" + mine_field.render(cursor_index) + f"\n{mine_field.get_flag_count()}/{mine_field.get_mine_count()}\nRECORDING: {DO_RECORD}\nPLAYBACK: {DO_PLAYBACK}")

def on_left_pressed():
	move_cursor(-1, 0)
def on_right_pressed():
	move_cursor(1, 0)
def on_up_pressed():
	move_cursor(0, -1)
def on_down_pressed():
	move_cursor(0, 1)
def on_flag_pressed():
	mine_field.flag_cell(*cursor)
def on_dig_pressed():
	mine_field.open_cell(*cursor)

KEYMAPPING = {
	"w": on_up_pressed,
	"a": on_left_pressed,
	"s": on_down_pressed,
	"d": on_right_pressed,

	"f": on_flag_pressed,
	"enter": on_dig_pressed
}

redraw_screen()

while not mine_field.is_exploded:
	if DO_PLAYBACK:
		sleep(0.01)
		key = playback_sequence[current_playback_index].strip()
		current_playback_index += 1
	else:
		key = keyboard.read_key()
		is_down = keyboard.is_pressed(key)

		if not is_down:
			continue # ignore release

		if DO_RECORD:
			playback_sequence.append(str(key))


	callback = KEYMAPPING.get(str(key))

	if callback == None:
		continue

	callback()

	if mine_field.is_win_state():
		on_win()
		break
	elif mine_field.is_exploded:
		on_lose()
		break

	redraw_screen()

if DO_RECORD:
	with open("playback_sequence.txt", "w") as f:
		f.write(f"{SEED}\n")
		f.writelines(f"{x}\n" for x in playback_sequence)

print("press esc to exit.")
keyboard.wait("esc")
