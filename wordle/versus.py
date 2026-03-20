from modules.formatting import format_guess, bold
from modules.game import WordleGame, DICTIONARY, choice
from modules.guesser import WordleGuesser
from modules.player import WordlePlayer

target_word = choice(DICTIONARY)

def format_games(human_game: WordleGame, bot_game: WordleGame) -> str:
	lines = []

	display_games = (human_game, bot_game)

	for index in range(max(len(game.guesses) for game in display_games)):
		line = f"{index + 1} > "
		for game in display_games:
			try:
				word, validity = game.guesses[index]
				display_word = "?" * len(target_word) if game != human_game and not human_game.is_over else word
				line += format_guess(display_word, validity) + "  "
			except:
				line += " " * (len(target_word) * 3) + "  "
		lines.append(line)

	return "\n".join(lines)

bot_game = WordleGame(secret_word=target_word)
bot_player = WordleGuesser(bot_game)

human_game = WordleGame(secret_word=target_word)
human_player = WordlePlayer(human_game)

print(f"\033[H\033[2J{bold("Versus Wordle")}\nGuess the secret {bold(str(len(target_word)))} letter word before the bot!\n")

while not human_game.is_over:
	if not bot_game.is_over:
		bot_player.make_guess(None if len(bot_game.guesses) > 0 else choice(DICTIONARY))
		print("Bot has made guess.")

	human_player.make_guess("Your guess")

	print("\x1b[2J\x1b[H" + format_games(human_game, bot_game))

if human_game.is_won == bot_game.is_won and len(human_game.guesses) == len(bot_game.guesses):
	print("You tied with the bot!")
elif human_game.is_won and len(human_game.guesses) <= len(bot_game.guesses):
	print("You won!")
else:
	print("You lost to the bot!")

print(f"The word was {bold(target_word)}.")