from random import Random
from pyansi import AnsiStyle, Palette, PaletteColor

# FIELD STATES
CLOSED = 0
OPEN = 1
MINE = 2

OFFETS_NORMAL = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]
OFFSETS_ORTHO = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
OFFSETS_DIAG = [ (-1, -1), (1, -1), (-1, 1), (1, 1) ]
OFFSETS_KNIGHT = [ (-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2) ]
MINE_CHECK_OFFSETS = OFFSETS_ORTHO

DANGER_STYLES = [ AnsiStyle(fg=Palette(PaletteColor.BrightBlue)), AnsiStyle(fg=Palette(PaletteColor.BrightGreen)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightRed)), AnsiStyle(fg=Palette(PaletteColor.BrightMagenta)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightCyan)), AnsiStyle(fg=Palette(PaletteColor.Yellow)),
				  AnsiStyle(fg=Palette(PaletteColor.Red)), AnsiStyle(fg=Palette(PaletteColor.BrightBlack)) ]
FLAG_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightYellow), bg=Palette(PaletteColor.Red))
CLOSED_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightBlack), bg=Palette(PaletteColor.BrightBlack))
HIGHLIGHT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightWhite), fg=Palette(PaletteColor.Black))

class Field:
	def __init__(self, width: int, height: int, seed: int) -> None:
		self._field = [CLOSED] * width * height
		self._flags = [False] * width * height

		self.is_exploded = False
		self.is_first_move = False

		self.width = width
		self.height = height

		self._rand = Random(seed)

	def read_field_state(self, x: int, y: int) -> int:
		return self._field[self.to_index(x, y)]
	def write_field_state(self, x: int, y: int, state: int):
		self._field[self.to_index(x, y)] = state
	def read_flag_state(self, x: int, y: int) -> bool:
		return self._flags[self.to_index(x, y)]
	def write_flag_state(self, x: int, y: int, is_flagged: bool):
		self._flags[self.to_index(x, y)] = is_flagged

	def within_bounds(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def to_index(self, x: int, y: int) -> int:
		return self.width * y + x
	
	def place_mine(self):
		while True:
				index = self._rand.randint(0, self.width * self.height - 1)

				if self._field[index] != MINE:
					self._field[index] = MINE

					break
	def place_mines(self, count: int):
		for _ in range(count):
			self.place_mine()

	def get_flag_count(self) -> int:
		count = 0	

		for is_flagged in self._flags:
			if is_flagged:
				count += 1
		
		return count
	def get_mine_count(self) -> int:
		count = 0

		for cell in self._field:
			if cell == MINE:
				count += 1
		
		return count
	def is_win_state(self):
		if self.is_exploded:
			return False

		all_flagged = True

		for cell, is_flagged in zip(self._field, self._flags):
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

			if self.read_field_state(check_x, check_y) == MINE:
				nearby += 1

		return nearby
	def get_nearby_flag_count(self, x: int, y: int) -> int:
		nearby = 0

		for offset_x, offset_y in MINE_CHECK_OFFSETS:
			check_x, check_y = x + offset_x, y + offset_y

			if not self.within_bounds(check_x, check_y):
				continue

			if self.read_flag_state(check_x, check_y):
				nearby += 1
		
		return nearby

	def ensure_safety(self, x: int, y: int):
		is_totally_safe = False

		while not is_totally_safe:
			is_totally_safe = True

			for off_x in range(-1, 2):
				for off_y in range(-1, 2):
					# off_index = self.to_index(x + off_x, y + off_y)
					check_x, check_y = x + off_x, y + off_y

					if self.read_field_state(check_x, check_y) == MINE:
						is_totally_safe = False

						self.write_field_state(check_x, check_y, CLOSED)
						self.place_mine()

	def open_cell(self, x: int, y: int) -> bool:
		if not self.within_bounds(x, y):
			return False

		index = self.to_index(x, y)

		if self._flags[index] == True:
			return False
		
		if self._field[index] == OPEN:
			return False
		
		if not self.is_first_move:
			self.is_first_move = True
			self.ensure_safety(x, y)

		if self._field[index] == MINE:
			self.is_exploded = True

			return True

		

		self._field[index] = OPEN

		if self.get_nearby_mine_count(x, y) == 0: # open neighboring cells
			for offset in MINE_CHECK_OFFSETS:
				off_x, off_y = offset
				self.open_cell(x + off_x, y + off_y)
		
		return True
	def flag_cell(self, x: int, y: int) -> bool:
		if not self.within_bounds(x, y):
			return False
		
		if self.read_field_state(x, y) == OPEN:
			return False
		
		self.write_flag_state(x, y, not self.read_flag_state(x, y))

		return True

	def render(self, highlight_index: int) -> str:
		output = ""

		for y in range(self.height):
			for x in range(self.width):
				index = y * self.width + x

				state = self.read_field_state(x, y)
				is_flagged = self.read_flag_state(x, y)
				is_highlighted = index == highlight_index

				px_style = None
				px = ""

				if state == OPEN:
					danger = self.get_nearby_mine_count(x, y)

					if danger == 0:
						px = ". "
					else:
						px = f"{danger} "

						if not is_highlighted:
							px_style = DANGER_STYLES[danger - 1]
				else:
					if is_flagged:
						px = "P "
						px_style = FLAG_STYLE
					else:
						px = "# "
						px_style = CLOSED_STYLE

				if is_highlighted:
					px_style = HIGHLIGHT_STYLE

				if px_style != None:
					px = px_style.apply_with_reset(px)

				output += px
					
			output += "\n"

		return output
