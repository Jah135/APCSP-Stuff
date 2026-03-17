from pyansi import AnsiStyle, PaletteColor, Palette, bold
from game import WordleGame, LetterValidity
from modules.guesser import WordleGuesser

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
		elif validity == LetterValidity.Incorrect or validity == LetterValidity.TooMany:
			output += INCORRECT_STYLE.apply_with_reset(display)

	return output

def render_game(game: WordleGame) -> str:
	output = "\x1b[2J\x1b[H\n"

	for guess_index, guess in enumerate(game.guesses):
		word, word_validity = guess

		output += f"{guess_index + 1} > {format_guess(word, word_validity)}\n"

	output += "\n"

	return output

game = WordleGame(max_guesses=6,secret_word=None)
player = WordleGuesser(game)

print(game.secret_word)

print(f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(game.secret_word)))} letter word!\n")
while True:
	current_guess_index = len(game.guesses) + 1
	word, _ = player.make_guess()

	print(render_game(game))

	if word == game.secret_word:
		print("You guessed the word!")
		break
	
	if current_guess_index >= game.max_guesses:
		print(f"Ran out of guesses.")
		break

print(f"The secret word was {bold(game.secret_word)}.")