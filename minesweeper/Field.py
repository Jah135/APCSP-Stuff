from random import Random
from pyansi import AnsiStyle, Palette, PaletteColor

CLOSED = 0
OPEN = 1
MINE = 2

MINE_CHECK_OFFSETS = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]

DANGER_STYLES = [ AnsiStyle(fg=Palette(PaletteColor.BrightBlue)), AnsiStyle(fg=Palette(PaletteColor.BrightGreen)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightRed)), AnsiStyle(fg=Palette(PaletteColor.BrightMagenta)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightCyan)), AnsiStyle(fg=Palette(PaletteColor.Yellow)),
				  AnsiStyle(fg=Palette(PaletteColor.Red)), AnsiStyle(fg=Palette(PaletteColor.BrightBlack)) ]
HIGHLIGHT_STYLE = AnsiStyle(bg=Palette(PaletteColor.Cyan), fg=Palette(PaletteColor.Black))
FLAG_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightYellow))

class Field:
	def __init__(self, width: int, height: int, seed: int) -> None:
		self.data = [CLOSED] * width * height
		self.flags = [False] * width * height
		self.is_dead = False

		self.width = width
		self.height = height

		self._rand = Random(seed)

	def within_bounds(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def to_index(self, x: int, y: int) -> int:
		return self.width * y + x
	
	def place_mines(self, count: int):
		for _ in range(count):
			while True:
				index = self._rand.randint(0, self.width * self.height - 1)

				if self.data[index] != MINE:
					self.data[index] = MINE

					break

	def get_flag_count(self) -> int:
		count = 0	

		for is_flagged in self.flags:
			if is_flagged:
				count += 1
		
		return count
	def get_mine_count(self) -> int:
		count = 0

		for cell in self.data:
			if cell == MINE:
				count += 1
		
		return count
	def is_win_state(self):
		if self.is_dead:
			return False

		all_flagged = True

		for cell, is_flagged in zip(self.data, self.flags):
			if cell == MINE and not is_flagged:
				all_flagged = False
				break
		
		return all_flagged
	
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
