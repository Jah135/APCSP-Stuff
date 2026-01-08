from random import choice
from pyansi import AnsiStyle, PaletteColor, Palette

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))

CORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black))
INCORRECT_STYLE = AnsiStyle(bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black))
EXISTS_STYLE = AnsiStyle(bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black))

with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]

SECRET_WORD = "godly" #choice(DICTIONARY)

MAX_GUESSES = 10
current_guess = 0

print(f"{AnsiStyle(flags=1).apply_with_reset("Simple Wordle")}\nGuess the {len(SECRET_WORD)} character word!\n")

def error(text: str):
	print(ERROR_STYLE.apply_with_reset(text))

while True:
	guess = input(f"Guess {current_guess}: ").lower()
	
	if len(guess) != len(SECRET_WORD):
		error("Invalid input length!")
		continue

	if guess not in DICTIONARY:
		error("Invalid word! (not in dictionary)")
		continue

	output = ""

	for index in range(len(SECRET_WORD)):
		guess_character = guess[index]
		render_character = f" {guess_character.upper()} "

		num_char_occurances = SECRET_WORD.count(guess_character, index)
		num_secr_occurances = guess.count(guess_character, index)

		print(num_char_occurances, num_secr_occurances, guess_character)

		if SECRET_WORD[index] == guess_character:
			output += CORRECT_STYLE.apply_with_reset(render_character)
		elif num_secr_occurances < num_char_occurances:
			output += EXISTS_STYLE.apply_with_reset(render_character)
		else:
			output += INCORRECT_STYLE.apply_with_reset(render_character)
		
		output += " "
	
	print(output)

	if guess == SECRET_WORD:
		print("You guessed the word!")
		break
	
	current_guess += 1

	if current_guess > MAX_GUESSES:
		print("Ran out of guesses")
		break