from pyansi import bold
from modules.formatting import render_game
from modules.game import WordleGame
from modules.player import HumanWordlePlayer

game = WordleGame(max_guesses=6)
player = HumanWordlePlayer(len(game.secret_word))

print(
    f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(game.secret_word)))} letter word!\n"
)
while True:
    current_guess_index = len(game.guesses) + 1
    word = player.prompt_word()

    player.on_guess_feedback(*game.make_guess(word))

    print(render_game(game))

    if game.is_won:
        print("You guessed the word!")
        break

    if game.is_over:
        print(f"Ran out of guesses.")
        break

print(f"The secret word was {bold(game.secret_word)}.")
