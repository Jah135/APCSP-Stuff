from random import choice
from pyansi import AnsiStyle, PaletteColor, Palette, bold

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))

CORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black))
INCORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black))
EXISTS_STYLE = AnsiStyle(bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black))
NEUTRAL_STYLE = AnsiStyle(bg=Palette(PaletteColor.White), fg=Palette(PaletteColor.Black))

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

SECRET_WORD = choice(DICTIONARY)

MAX_GUESSES = 6
guesses = []


print(f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(SECRET_WORD)))} letter word!\n")

def error(text: str):
	print(ERROR_STYLE.apply_with_reset(text))

def format_guess(guess: str) -> str:
	available_counts = { char:SECRET_WORD.count(char) for char in guess }

	for secret_char, guess_char in zip(SECRET_WORD, guess):
		if guess_char == secret_char:
			available_counts[guess_char] -= 1
	
	output = ""

	for secret_char, guess_char in zip(SECRET_WORD, guess):
		is_correct = secret_char == guess_char
		exists_in_secret = available_counts.get(guess_char, 0) > 0

		available_counts[guess_char] -= 1

		render_char = f" {guess_char.upper()} "

		if is_correct:
			output += CORRECT_STYLE.apply_with_reset(render_char)
		elif not is_correct and exists_in_secret:
			output += EXISTS_STYLE.apply_with_reset(render_char)
		else:
			output += INCORRECT_STYLE.apply_with_reset(render_char)

	return output

def render_screen() -> str:
	output = "\x1b[2J\x1b[H"

	for index, guess in enumerate(guesses):
		output += f"{index + 1} > {format_guess(guess)}\n"

	return output

while True:
	current_guess_index = len(guesses) + 1
	player_guess = input(f"Guess {current_guess_index}/{MAX_GUESSES}: ").lower()
	
	if player_guess not in DICTIONARY:
		error("Invalid word! (not in dictionary)")
		continue

	guesses.append(player_guess)

	print(render_screen())

	if player_guess == SECRET_WORD:
		print("You guessed the word!")
		break
	
	if current_guess_index >= MAX_GUESSES:
		print(f"Ran out of guesses.")
		break

print(f"The secret word was {bold(SECRET_WORD)}.")