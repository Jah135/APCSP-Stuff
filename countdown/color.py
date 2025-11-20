from enum import IntEnum

class PaletteColor(IntEnum):
	Black = 30
	Red = 31
	Green = 32
	Yellow = 33
	Blue = 34
	Magenta = 35
	Cyan = 36
	White = 37

	BrightBlack = 90
	BrightRed = 91
	BrightGreen = 92
	BrightYellow = 93
	BrightBlue = 94
	BrightMagenta = 95
	BrightCyan = 96
	BrightWhite = 97

	Default = 39

# Abstract AnsiColor class
class AnsiColor:
	def get_sequence(self, background: bool) -> str:
		...

class Palette(AnsiColor):
	def __init__(self, code: int) -> None:
		self.code = code
	
	def get_sequence(self, background: bool) -> str:
		code = self.code

		if background:
			code += 10
		
		return str(code)
class RGB8bit(AnsiColor):
	def __init__(self, index: int) -> None:
		self.index = index

	def get_sequence(self, background: bool) -> str:
		return generate_8bit_sequence(self.index, background=background)
class RGB24bit(AnsiColor):
	def __init__(self, red: int, green: int, blue: int) -> None:
		self.color = (red, green, blue)
	
	def get_sequence(self, background: bool) -> str:
		return generate_24bit_sequence(*self.color, background=background)

def generate_8bit_sequence(code: int, background: bool = False):
	return f"{background and "48" or "38"};5;{code}"
def generate_24bit_sequence(r: int, g: int, b: int, background: bool = False):
	return f"{background and "48" or "38"};2;{r};{g};{b}"