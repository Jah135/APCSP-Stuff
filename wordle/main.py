from random import choice
from pyansi import AnsiStyle, PaletteColor, Palette

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))

CORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black))
INCORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black))
EXISTS_STYLE = AnsiStyle(bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black))

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

SECRET_WORD = choice(DICTIONARY)

remaining_guesses = 10

print(f"{AnsiStyle(flags=1).apply_with_reset("Simple Wordle")}\nGuess the {len(SECRET_WORD)} character word!\n")


def error(text: str):
	print(ERROR_STYLE.apply_with_reset(text))

while True:
	guess = input(f"Guess {remaining_guesses}: ").lower()
	
	if len(guess) != len(SECRET_WORD):
		error("Invalid input length!")
		continue

	if guess not in DICTIONARY:
		error("Invalid word! (not in dictionary)")
		continue

	output = ""

	start_indices = {}

	for index in range(len(SECRET_WORD)):
		guess_char = guess[index]
		render_char = f" {guess_char.upper()} "

		find_index = SECRET_WORD.find(guess_char, start_indices.get(guess_char))

		if SECRET_WORD[index] == guess_char:
			output += CORRECT_STYLE.apply_with_reset(render_char)
		elif find_index != -1:
			start_indices[guess_char] = find_index + 1

			output += EXISTS_STYLE.apply_with_reset(render_char)
		else:
			output += INCORRECT_STYLE.apply_with_reset(render_char)
		
		output += " "
	
	print(output)

	if guess == SECRET_WORD:
		print("You guessed the word!")
		break
	
	remaining_guesses -= 1

	if remaining_guesses <= 0:
		print("Ran out of guesses")
		break