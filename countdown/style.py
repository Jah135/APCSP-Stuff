from typing import Self, Tuple, Optional
from color import AnsiColor

BOLD_MASK = 0b1
ITALIC_MASK = 0b10
DIM_MASK = 0b100
UNDERLINE_MASK = 0b1000
STRIKETHROUGH_MASK = 0b10000

class AnsiStyle:
	def __init__(self, *_, fg: Optional[AnsiColor] = None, bg: Optional[AnsiColor] = None, flags: int = 0):
		self.foreground = fg
		self.background = bg
		self.flags = flags
	
	def __str__(self) -> str:
		if self.__is_plain():
			return ""

		output = "\x1b["

		_wrote = False;
		def _append(text: str):
			nonlocal output
			nonlocal _wrote

			if _wrote:
				output += ";"
			
			output += text
			_wrote = True

		if self.__get_flag(BOLD_MASK):
			_append("1")
		if self.__get_flag(DIM_MASK):
			_append("2")
		if self.__get_flag(ITALIC_MASK):
			_append("3")
		if self.__get_flag(UNDERLINE_MASK):
			_append("4")
		if self.__get_flag(STRIKETHROUGH_MASK):
			_append("9")

		if self.foreground != None:
			_append(self.foreground.get_sequence(False))
		if self.background != None:
			_append(self.background.get_sequence(True))

		output += "m"

		return output

	def __is_plain(self) -> bool:
		return self.foreground == None and self.background == None and self.flags == 0
	def __set_flag(self, mask: int, enabled: bool) -> Self:
		if enabled:
			self.flags |= mask
		else:
			self.flags &= ~mask
		
		return self
	def __get_flag(self, mask: int) -> bool:
		return self.flags & mask == mask

	def fg(self, color: Optional[AnsiColor]) -> Self:
		self.foreground = color
		return self
	def bg(self, color: Optional[AnsiColor]) -> Self:
		self.background = color
		return self

	def bold(self, enabled: bool = True) -> Self:
		return self.__set_flag(BOLD_MASK, enabled)
	def italic(self, enabled: bool = True) -> Self:
		return self.__set_flag(ITALIC_MASK, enabled)
	def dim(self, enabled: bool = True) -> Self:
		return self.__set_flag(DIM_MASK, enabled)
	def underline(self, enabled: bool = True) -> Self:
		return self.__set_flag(UNDERLINE_MASK, enabled)
	def strikethrough(self, enabled: bool = True) -> Self:
		return self.__set_flag(STRIKETHROUGH_MASK, enabled)