from pyansi import AnsiStyle, PaletteColor, Palette, bold
from game import WordleGame, DICTIONARY

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))

def error(text: str):
	print(ERROR_STYLE.apply_with_reset(text))

class WordlePlayer:
	def __init__(self, game: WordleGame) -> None:
		self.game = game
	
	def prompt_guess(self):
		while True:
			player_guess = input("Guess: ")

			guess_len = len(player_guess)
			secret_len = len(self.game.secret_word)

			if guess_len < secret_len:
				error(f"Not enough letters. ({guess_len} < {secret_len})")
				continue
			elif guess_len > secret_len:
				error(f"Too many letters. ({guess_len} > {secret_len})")
				continue
			elif player_guess not in DICTIONARY:
				error("Word not in dictionary.")
				continue
			
			break

		return self.game.make_guess(player_guess)