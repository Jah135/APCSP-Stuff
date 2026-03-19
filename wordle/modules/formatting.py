from pyansi import AnsiStyle, PaletteColor, Palette
from modules.game import WordleGame, LetterValidity

CORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black))
INCORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black))
EXISTS_STYLE = AnsiStyle(bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black))
NEUTRAL_STYLE = AnsiStyle(bg=Palette(PaletteColor.White), fg=Palette(PaletteColor.Black))

def format_guess(guess: str, guess_validity: list[LetterValidity]) -> str:
	output = ""

	for char, validity in zip(guess, guess_validity):
		display = f" {char.upper()} "
		if validity == LetterValidity.Correct:
			output += CORRECT_STYLE.apply_with_reset(display)
		elif validity == LetterValidity.Exists:
			output += EXISTS_STYLE.apply_with_reset(display)
		else:
			output += INCORRECT_STYLE.apply_with_reset(display)

	return output

def render_game(game: WordleGame) -> str:
	output = "\x1b[2J\x1b[H\n"

	for guess_index, guess in enumerate(game.guesses):
		word, word_validity = guess

		output += f"{guess_index + 1} > {format_guess(word, word_validity)}\n"

	output += "\n"

	return output
