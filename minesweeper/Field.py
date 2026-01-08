from random import Random
from pyansi import AnsiStyle, Palette, PaletteColor

# FIELD STATES
CLOSED = 0b01
OPEN = 0b10
MINE = 0b11
FLAGGED = 0b100

MAX_SAFETY_ATTEMPTS = 8
SHOW_OFFSETS = True

OFFSETS_NORMAL = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]
OFFSETS_ORTHO = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
OFFSETS_ORTHO_FAR = [ (-2, 0), (-1, 0), (2, 0), (1, 0), (0, -2), (0, -1), (0, 2), (0, 1) ]
OFFSETS_DIAG = [ (-1, -1), (1, -1), (-1, 1), (1, 1) ]
OFFSETS_KNIGHT = [ (-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2) ]
MINE_CHECK_OFFSETS = OFFSETS_ORTHO_FAR

DANGER_STYLES = [ AnsiStyle(fg=Palette(PaletteColor.BrightBlue)), AnsiStyle(fg=Palette(PaletteColor.BrightGreen)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightRed)), AnsiStyle(fg=Palette(PaletteColor.BrightMagenta)),
				  AnsiStyle(fg=Palette(PaletteColor.BrightCyan)), AnsiStyle(fg=Palette(PaletteColor.Yellow)),
				  AnsiStyle(fg=Palette(PaletteColor.Red)), AnsiStyle(fg=Palette(PaletteColor.BrightBlack)) ]
FLAG_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightYellow), bg=Palette(PaletteColor.Red))
CLOSED_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightBlack), bg=Palette(PaletteColor.BrightBlack))
HIGHLIGHT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightWhite), fg=Palette(PaletteColor.Black))

# Returns field type
def extract_type(state: int) -> int:
	return state & ~FLAGGED
# Returns whether the state is flagged
def extract_flagged(state: int) -> bool:
	return state & FLAGGED != 0

class Field:
	def __init__(self, width: int, height: int, seed: int) -> None:
		self._field = bytearray(width * height)

		self.is_exploded = False
		self.is_first_move = False

		self.width = width
		self.height = height

		self._rand = Random(seed)

	def _read_field(self, index: int) -> int:
		return self._field[index] & ~FLAGGED
	def read_field(self, x: int, y: int) -> int:
		return self._read_field(self.to_index(x, y))
	
	def _write_field(self, index: int, new_state: int):
		self._field[index] |= new_state & ~FLAGGED
	def write_field(self, x: int, y: int, state: int):
		self._write_field(self.to_index(x, y), state)
	
	def _read_flag(self, index: int) -> bool:
		return self._field[index] & FLAGGED != 0
	def read_flag(self, x: int, y: int) -> bool:
		return self._read_flag(self.to_index(x, y))
	
	def _write_flag(self, index: int, is_flagged: bool):
		if is_flagged:
			self._field[index] |= FLAGGED
		else:
			self._field[index] &= ~FLAGGED
	def write_flag(self, x: int, y: int, is_flagged: bool):
		self._write_flag(self.to_index(x, y), is_flagged)
			

	def within_bounds(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def to_index(self, x: int, y: int) -> int:
		return self.width * y + x
	
	def place_mine(self):
		while True:
			index = self._rand.randint(0, self.width * self.height - 1)

			if self._read_field(index) != MINE:
				self._write_field(index, MINE)
				break
	def place_mines(self, count: int):
		for _ in range(count):
			self.place_mine()

	def get_flag_count(self) -> int:
		count = 0	

		for state in self._field:
			if extract_flagged(state):
				count += 1
		
		return count
	def get_mine_count(self) -> int:
		count = 0

		for state in self._field:
			if extract_type(state) == MINE:
				count += 1
		
		return count
	def is_win_state(self):
		if self.is_exploded:
			return False

		all_flagged = True

		for state in self._field:
			if extract_type(state) == MINE and not extract_flagged(state):
				all_flagged = False
				break
		
		return all_flagged
	
	def get_nearby_mine_count(self, x: int, y: int) -> int:
		nearby = 0

		for offset_x, offset_y in MINE_CHECK_OFFSETS:
			check_x, check_y = x + offset_x, y + offset_y

			if not self.within_bounds(check_x, check_y):
				continue

			if self.read_field(check_x, check_y) == MINE:
				nearby += 1

		return nearby
	def get_nearby_flag_count(self, x: int, y: int) -> int:
		nearby = 0

		for offset_x, offset_y in MINE_CHECK_OFFSETS:
			check_x, check_y = x + offset_x, y + offset_y

			if not self.within_bounds(check_x, check_y):
				continue

			if self.read_flag(check_x, check_y):
				nearby += 1
		
		return nearby

	def ensure_safety(self, x: int, y: int):
		is_totally_safe = False

		attempts = 0

		while not is_totally_safe:
			if attempts > MAX_SAFETY_ATTEMPTS:
				print("MAXIMUM SAFETY ATTEMPTS EXCEEDED!")
				break

			attempts += 1
			is_totally_safe = True

			for off_x in range(-1, 2):
				for off_y in range(-1, 2):
					# off_index = self.to_index(x + off_x, y + off_y)
					check_x, check_y = x + off_x, y + off_y

					if self.read_field(check_x, check_y) == MINE:
						is_totally_safe = False

						self.write_field(check_x, check_y, CLOSED)
						# self.place_mine()

	def player_open_cell(self, x: int, y: int, do_recurse: bool = True) -> bool:
		if not self.within_bounds(x, y):
			return False

		index = self.to_index(x, y)

		if self._read_flag(index):
			return False
		
		danger = self.get_nearby_mine_count(x, y)

		if self._read_field(index) == OPEN:
			# CHORDING
			if do_recurse and danger == self.get_nearby_flag_count(x, y):
				for off_x, off_y in MINE_CHECK_OFFSETS:
					self.player_open_cell(x + off_x, y + off_y, do_recurse=False)
				
				return True

			return False

		if not self.is_first_move:
			self.is_first_move = True
			self.ensure_safety(x, y)

		if self._read_field(index) == MINE:
			self.is_exploded = True

			return True

		self._write_field(index, OPEN)

		if danger == 0: # open neighboring cells
			for off_x, off_y in MINE_CHECK_OFFSETS:
				self.player_open_cell(x + off_x, y + off_y)
		
		return True
	def player_flag_cell(self, x: int, y: int) -> bool:
		if not self.within_bounds(x, y):
			return False
		
		if self.read_field(x, y) == OPEN:
			return False
		
		self.write_flag(x, y, not self.read_flag(x, y))

		return True

	def render(self, cursor_position: tuple[int, int]) -> str:
		output = ""

		highlight_indices = [self.to_index(*cursor_position)]

		if SHOW_OFFSETS:
			for off_x, off_y in MINE_CHECK_OFFSETS:
				check_x, check_y = cursor_position[0] + off_x, cursor_position[1] + off_y

				if not self.within_bounds(check_x, check_y):
					continue

				highlight_indices.append(self.to_index(check_x, check_y))

		for y in range(self.height):
			for x in range(self.width):
				index = y * self.width + x

				state = self.read_field(x, y)
				is_flagged = self.read_flag(x, y)
				is_highlighted = index in highlight_indices



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
