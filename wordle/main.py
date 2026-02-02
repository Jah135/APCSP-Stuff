from random import choice
from pyansi import AnsiStyle, PaletteColor, Palette, bold

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))

CORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black))
INCORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black))
EXISTS_STYLE = AnsiStyle(bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black))
NEUTRAL_STYLE = AnsiStyle(bg=Palette(PaletteColor.White), fg=Palette(PaletteColor.Black))

KEYBOARD = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

SECRET_WORD = choice(DICTIONARY)

MAX_GUESSES = 6
current_guess = 0

print(f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(SECRET_WORD)))} letter word!\n")

def error(text: str):
	print(ERROR_STYLE.apply_with_reset(text))

def render_keyboard(correct_chars: str, exists_chars: str, incorrect_chars: str) -> str:
	output = ""

	for row in KEYBOARD:
		for char in row:
			style = NEUTRAL_STYLE

			if char in correct_chars:
				style = CORRECT_STYLE
			elif char in exists_chars:
				style = EXISTS_STYLE
			elif char in incorrect_chars:
				style = INCORRECT_STYLE

			output += style.apply_with_reset(f" {char.upper()} ") + " "
		output += "\n"

	return output

CORRECT_CHARS = ""
EXISTS_CHARS = ""
INCORRECT_CHARS = ""

while True:
	guess_word = input(f"Guess {current_guess + 1}/{MAX_GUESSES}: ").lower()
	
	if guess_word not in DICTIONARY:
		error("Invalid word! (not in dictionary)")
		continue

	formatted_guess = ""

	# there's probably a better way to do this
	# count up "available" characters (for determining if the character is in the word and not in the correct position)
	available_counts = { char:SECRET_WORD.count(char) for char in guess_word }

	# decrement "invalid" characters (characters already in the correct position)
	for secret_char, guess_char in zip(SECRET_WORD, guess_word):
		if guess_char == secret_char:
			available_counts[guess_char] -= 1

	for index, secret_char, guess_char in zip(range(len(SECRET_WORD)), SECRET_WORD, guess_word):
		is_correct = secret_char == guess_char
		exists_in_secret = available_counts.get(guess_char, 0) > 0

		if is_correct and not guess_char in CORRECT_CHARS:
			CORRECT_CHARS += guess_char
		elif exists_in_secret and not guess_char in EXISTS_CHARS:
			EXISTS_CHARS += guess_char
		elif not guess_char in INCORRECT_CHARS:
			INCORRECT_CHARS += guess_char

		available_counts[guess_char] -= 1

		render_char = f" {guess_char.upper()} "

		if is_correct:
			formatted_guess += CORRECT_STYLE.apply_with_reset(render_char)
		elif not is_correct and exists_in_secret:
			formatted_guess += EXISTS_STYLE.apply_with_reset(render_char)
		else:
			formatted_guess += INCORRECT_STYLE.apply_with_reset(render_char)
		
		formatted_guess += " "
	
	print(formatted_guess + "\n")
	print(render_keyboard(CORRECT_CHARS, EXISTS_CHARS, INCORRECT_CHARS))

	if guess_word == SECRET_WORD:
		print("You guessed the word!")
		break
	
	current_guess += 1

	if current_guess >= MAX_GUESSES:
		print(f"Ran out of guesses.")
		break

print(f"The secret word was {bold(SECRET_WORD)}.")