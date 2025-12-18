from pyansi import AnsiStyle, Palette, PaletteColor
from random import randint
from keyboard import add_hotkey

CLOSED = 0
OPEN = 1
MINE = 2

MINE_CHECK_OFFSETS = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]
DANGER_STYLES = [ AnsiStyle(fg=Palette(PaletteColor.BrightBlue)), AnsiStyle(fg=Palette(PaletteColor.BrightGreen)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightRed)), AnsiStyle(fg=Palette(PaletteColor.BrightMagenta)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightCyan)), AnsiStyle(fg=Palette(PaletteColor.BrightYellow)),
				  AnsiStyle(fg=Palette(PaletteColor.Red)), AnsiStyle(fg=Palette(PaletteColor.BrightBlack)) ]
HIGHLIGHT_STYLE = AnsiStyle(bg=Palette(PaletteColor.Cyan), fg=Palette(PaletteColor.Black))

class Field:
	def __init__(self, width: int, height: int) -> None:
		self.data = [CLOSED] * width * height
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
	def open_cell(self, x: int, y: int):
		if not self.within_bounds(x, y):
			return

		index = self.to_index(x, y)

		if self.data[index] == OPEN:
			return

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

	def render(self, highlight_index: int) -> str:
		output = ""

		for y in range(self.height):
			for x in range(self.width):
				index = y * self.width + x
				val = self.data[index]

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
				else: #val == CLOSED:
					px = "# "
				# elif val == MINE:
				# 	output += "X "

				if is_highlighted:
					px = HIGHLIGHT_STYLE.apply_with_reset(px)

				output += px
					
			output += "\n"

		return output

cursor = (0, 0)

new_field = Field(30, 10)
new_field.place_mines(40)

print(new_field.render(0))

new_field.open_cell(0, 0)
new_field.open_cell(5, 5)

print(new_field.render(0))