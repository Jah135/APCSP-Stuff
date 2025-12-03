from pyansi import AnsiStyle, RGB24bit
from constants import *

CELL_BG = AnsiStyle(bg=RGB24bit(180, 130, 40))
CELL_ALT_BG = AnsiStyle(bg=RGB24bit(100, 50, 20))

WHITE_FG = AnsiStyle(fg=RGB24bit(255, 255, 255)).bold()
BLACK_FG = AnsiStyle(fg=RGB24bit(20, 20, 20)).bold()

class ChessBoard:
	def __init__(self) -> None:
		self.data = [EMPTY] * HEIGHT * WIDTH
	
	def contains(self, x: int, y: int) -> bool:
		return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT
	def get_index(self, x: int, y: int) -> int:
		return x + WIDTH * y
	
	def set_piece(self, x: int, y: int, piece: int):
		self.data[self.get_index(x, y)] = piece
	def get_piece(self, x: int, y: int) -> int:
		return self.data[self.get_index(x, y)]

	def move_piece(self, x: int, y: int, target_x: int, target_y: int):
		self.set_piece(target_x, target_y, self.get_piece(x, y))
		self.set_piece(x, y, EMPTY)

	def render(self) -> str:
		output = ""

		for y in range(HEIGHT):
			output += f"{ALPHABET[y]}  "

			for x in range(WIDTH):
				piece = self.get_piece(x, y)

				is_white = piece & WHITE_MASK != 0
				piece_type = piece & TYPE_MASK
				name = PIECE_NAMES[piece_type]

				bg_style = CELL_ALT_BG if (x + y) & 1 != 0 else CELL_BG
				fg_style = WHITE_FG if is_white else BLACK_FG
				
				output += fg_style.apply(bg_style.apply_with_reset(name))

			output += "\n"

		output += "\n   "

		for x in range(WIDTH):
			output += f"{x + 1} "

		return output

board = ChessBoard()
board.set_piece(0, 0, PAWN)