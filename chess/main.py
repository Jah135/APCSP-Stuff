from pyansi import AnsiStyle, RGB24bit
from constants import *

CELL_BG = AnsiStyle(bg=RGB24bit(180, 130, 40))
CELL_ALT_BG = AnsiStyle(bg=RGB24bit(100, 50, 20))
HIGHLIGHT_BG = AnsiStyle(bg=RGB24bit(0, 255, 127))

WHITE_FG = AnsiStyle(fg=RGB24bit(255, 255, 255)).bold()
BLACK_FG = AnsiStyle(fg=RGB24bit(20, 20, 20)).bold()

def is_piece_white(piece: int) -> bool:
	return piece & 8 != 0
def get_piece_type(piece: int) -> int:
	return piece & 7

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

	def get_moves(self, x: int, y: int) -> list[int]:
		moves = []

		piece = self.get_piece(x, y)
		piece_type = get_piece_type(piece)

		if piece_type == PAWN:
			dir = -1 if is_piece_white(piece) else 1

			moves.append(self.get_index(x, y + dir))
		elif piece_type == KNIGHT:
			for knight_x, knight_y in KNIGHT_OFFSETS:
				final_x, final_y = knight_x + x, knight_y + y

				if self.contains(final_x, final_y):
					moves.append(self.get_index(final_x, final_y))
		elif piece == ROOK:
			for dir_index in range(0, 4):
				dir_x, dir_y = DIRECTION_OFFSETS[dir_index]

				for d in range(1, 8):
					off_x, off_y = dir_x * d, dir_y * d
					final_x, final_y = off_x + x, off_y + y

					if not self.contains(final_x, final_y):
						break

					moves.append(self.get_index(final_x, final_y))
		elif piece == BISHOP:
			for dir_index in range(4, 8):
				dir_x, dir_y = DIRECTION_OFFSETS[dir_index]

				for d in range(1, 8):
					off_x, off_y = dir_x * d, dir_y * d
					final_x, final_y = off_x + x, off_y + y

					if not self.contains(final_x, final_y):
						break

					moves.append(self.get_index(final_x, final_y))
		elif piece == QUEEN:
			for dir_index in range(8):
				dir_x, dir_y = DIRECTION_OFFSETS[dir_index]

				for d in range(1, 8):
					off_x, off_y = dir_x * d, dir_y * d
					final_x, final_y = off_x + x, off_y + y

					if not self.contains(final_x, final_y):
						break

					moves.append(self.get_index(final_x, final_y))
		elif piece == KING:
			for dir_index in range(8):
				dir_x, dir_y = DIRECTION_OFFSETS[dir_index]
				final_x, final_y = dir_x + x, dir_y + y

				if not self.contains(final_x, final_y):
					break

				moves.append(self.get_index(final_x, final_y))

		return moves

	def render(self, highlight_indices: list[int]) -> str:
		output = ""

		for y in range(HEIGHT):
			output += f"{ALPHABET[y]}  "

			for x in range(WIDTH):
				index = self.get_index(x, y)
				piece = self.get_piece(x, y)

				name = PIECE_NAMES[get_piece_type(piece)]

				bg_style = HIGHLIGHT_BG if index in highlight_indices else CELL_ALT_BG if (x + y) & 1 != 0 else CELL_BG
				fg_style = WHITE_FG if is_piece_white(piece) else BLACK_FG
				
				output += fg_style.apply(bg_style.apply_with_reset(name))

			output += "\n"

		output += "\n   "

		for x in range(WIDTH):
			output += f"{x + 1} "

		return output

board = ChessBoard()
board.set_piece(5, 5, PAWN | 8)

moves = board.get_moves(5, 5)
print(board.render(moves))