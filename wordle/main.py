from random import choice
from pyansi import AnsiStyle, PaletteColor, Palette, bold
from game import WordleGame, LetterValidity, check_word

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))

CORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black))
INCORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black))
EXISTS_STYLE = AnsiStyle(bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black))
NEUTRAL_STYLE = AnsiStyle(bg=Palette(PaletteColor.White), fg=Palette(PaletteColor.Black))

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

GAME = WordleGame(6)

print(f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(GAME.secret_word)))} letter word!\n")

def error(text: str):
	print(ERROR_STYLE.apply_with_reset(text))

def format_guess(guess: str, game: WordleGame) -> str:
	output = ""

	for char, validity in zip(guess, check_word(guess, game.secret_word)):
		display = f" {char.upper()} "
		if validity == LetterValidity.Correct:
			output += CORRECT_STYLE.apply_with_reset(display)
		elif validity == LetterValidity.Exists:
			output += EXISTS_STYLE.apply_with_reset(display)
		elif validity == LetterValidity.Incorrect:
			output += INCORRECT_STYLE.apply_with_reset(display)

	return output

def render_game(game: WordleGame) -> str:
	output = "\x1b[2J\x1b[H"

	for index, guess in enumerate(game.guesses):
		output += f"{index + 1} > {format_guess(guess, game)}\n"

	return output

while True:
	current_guess_index = len(GAME.guesses) + 1
	player_guess = input(f"Guess {current_guess_index}/{GAME.max_guesses}: ").lower()
	
	if player_guess not in DICTIONARY:
		error("Invalid word! (not in dictionary)")
		continue
	
	validity = GAME.make_guess(player_guess)
	# guesses.append(player_guess)

	print(render_game(GAME))

	if player_guess == GAME.secret_word:
		print("You guessed the word!")
		break
	
	if current_guess_index >= GAME.max_guesses:
		print(f"Ran out of guesses.")
		break

print(f"The secret word was {bold(GAME.secret_word)}.")