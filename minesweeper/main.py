from pyansi import AnsiStyle, Palette, PaletteColor
from random import randint
import keyboard
from os import system

CLOSED = 0
OPEN = 1
MINE = 2
FLAG = 3

MINE_CHECK_OFFSETS = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]
DANGER_STYLES = [ AnsiStyle(fg=Palette(PaletteColor.BrightBlue)), AnsiStyle(fg=Palette(PaletteColor.BrightGreen)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightRed)), AnsiStyle(fg=Palette(PaletteColor.BrightMagenta)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightCyan)), AnsiStyle(fg=Palette(PaletteColor.BrightYellow)),
				  AnsiStyle(fg=Palette(PaletteColor.Red)), AnsiStyle(fg=Palette(PaletteColor.BrightBlack)) ]
HIGHLIGHT_STYLE = AnsiStyle(bg=Palette(PaletteColor.Cyan), fg=Palette(PaletteColor.Black))
FLAG_STYLE = AnsiStyle(fg=Palette(PaletteColor.Yellow))

class Field:
	def __init__(self, width: int, height: int) -> None:
		self.data = [CLOSED] * width * height
		self.flags = [False] * width * height
		self.is_dead = False

		self.width = width
		self.height = height

	def within_bounds(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def to_index(self, x: int, y: int) -> int:
		return self.width * y + x
	
	def place_mines(self, count: int):
		for _ in range(count):
			while True:
				index = randint(0, self.width * self.height - 1)

				if self.data[index] != MINE:
					self.data[index] = MINE

					break

	def get_nearby_mine_count(self, x: int, y: int) -> int:
		nearby = 0

		for offset_x, offset_y in MINE_CHECK_OFFSETS:
			check_x, check_y = x + offset_x, y + offset_y

			if not self.within_bounds(check_x, check_y):
				continue

			index = self.to_index(check_x, check_y)

			if self.data[index] == MINE:
				nearby += 1

		return nearby
	
	def open_cell(self, x: int, y: int) -> bool:
		if not self.within_bounds(x, y):
			return False

		index = self.to_index(x, y)

		if self.flags[index] == True:
			return False
		
		if self.data[index] == MINE:
			self.is_dead = True

			return True

		if self.data[index] == OPEN:
			return False
		

		self.data[index] = OPEN

		if self.get_nearby_mine_count(x, y) == 0: # open neighboring cells
			self.open_cell(x - 1, y - 1)
			self.open_cell(x, y - 1)
			self.open_cell(x + 1, y - 1)
			self.open_cell(x - 1, y)
			self.open_cell(x + 1, y)
			self.open_cell(x - 1, y + 1)
			self.open_cell(x, y + 1)
			self.open_cell(x + 1, y + 1)
		
		return True
	def flag_cell(self, x: int, y: int) -> bool:
		if not self.within_bounds(x, y):
			return False
		
		index = self.to_index(x, y)

		if self.data[index] == OPEN:
			return False
		
		self.flags[index] = not self.flags[index]

		return True

	def render(self, highlight_index: int) -> str:
		output = ""

		for y in range(self.height):
			for x in range(self.width):
				index = y * self.width + x

				val = self.data[index]
				is_flagged = self.flags[index]
				is_highlighted = index == highlight_index

				px = ""

				if val == OPEN:
					danger = self.get_nearby_mine_count(x, y)

					if danger == 0:
						px = ". "
					else:
						px = f"{danger} "

						if not is_highlighted:
							style = DANGER_STYLES[danger - 1]
							px = style.apply_with_reset(px)
				else:
					if is_flagged:
						px = FLAG_STYLE.apply_with_reset("P ")
					else:
						px = "# "

				if is_highlighted:
					px = HIGHLIGHT_STYLE.apply_with_reset(px)

				output += px
					
			output += "\n"

		return output

cursor = (0, 0)

new_field = Field(15, 15)
new_field.place_mines(30)

def clamp(value: int, min_val: int, max_val: int): 
	return max(min(value, max_val), min_val)

def move_cursor(dx: int, dy: int):
	global cursor

	cursor = (
		clamp(cursor[0] + dx, 0, new_field.width - 1),
		clamp(cursor[1] + dy, 0, new_field.height - 1)
	)
def update_screen():
	if new_field.is_dead:
		print("YOU SUCK")
		keyboard.clear_all_hotkeys()
		exit()

	cursor_index = new_field.to_index(*cursor)

	system("cls")
	print(new_field.render(cursor_index))

def on_left_pressed():
	move_cursor(-1, 0)
	update_screen()
def on_right_pressed():
	move_cursor(1, 0)
	update_screen()
def on_up_pressed():
	move_cursor(0, -1)
	update_screen()
def on_down_pressed():
	move_cursor(0, 1)
	update_screen()
def on_f_pressed():
	if not new_field.flag_cell(*cursor):
		return
	
	update_screen()
def on_enter_pressed():
	if not new_field.open_cell(*cursor):
		return
	
	update_screen()

update_screen()

keyboard.add_hotkey("left", on_left_pressed)
keyboard.add_hotkey("right", on_right_pressed)
keyboard.add_hotkey("up", on_up_pressed)
keyboard.add_hotkey("down", on_down_pressed)
keyboard.add_hotkey("enter", on_enter_pressed)
keyboard.add_hotkey("f", on_f_pressed)
keyboard.wait("esc")
keyboard.clear_all_hotkeys()