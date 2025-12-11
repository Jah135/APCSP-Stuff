WIDTH = 8
HEIGHT = 8

# DIRECTION_OFFSETS = [ -WIDTH, WIDTH, -1, 1, -WIDTH - 1, -WIDTH + 1, WIDTH - 1, WIDTH + 1 ]
# KNIGHT_OFFSETS = [-WIDTH * 2 - 1, -WIDTH * 2 + 1, -WIDTH - 2, -WIDTH + 2, WIDTH - 2, WIDTH + 2, WIDTH * 2 - 1, WIDTH * 2 + 1]
DIRECTION_OFFSETS: list[tuple[int, int]] = [ (0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1) ]
KNIGHT_OFFSETS: list[tuple[int, int]] = [ (-1, 2), (1, 2), (-2, 1), (2, 1), (-2, -1), (2, -1), (-1, -2), (1, -2) ]

EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
PIECE_NAMES = ["  ", "P ", "K ", "B ", "R ", "Q ", "KI"]

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
