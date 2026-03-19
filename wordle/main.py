from pyansi import bold
from modules.formatting import render_game
from modules.game import WordleGame
from modules.guesser import WordleGuesser
from modules.player import WordlePlayer

if __name__ == "__main__":
	game = WordleGame(max_guesses=6, secret_word="quoin")
	player = WordleGuesser(game)

	print(f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(game.secret_word)))} letter word!\n")
	while True:
		current_guess_index = len(game.guesses) + 1
		word, _ = player.make_guess()

		print(render_game(game))

		if game.is_won:
			print("You guessed the word!")
			break
		
		if game.is_over:
			print(f"Ran out of guesses.")
			break

	print(f"The secret word was {bold(game.secret_word)}.")