from pyansi import bold
from modules.formatting import render_game
from modules.player import HumanWordlePlayer
from wordle import LocalWordleGame
from random import choice
from modules.guesser import WordleGuesser

game = LocalWordleGame(choice(WORD_DICTIONARY), max_guesses=6)
player = WordleGuesser(game, PLAYABLE_DICTIONARY)

print(
    f"\033[H\033[2J{bold("Simple Wordle")}\nGuess the secret {bold(str(len(game.secret_word)))} letter word!\n"
)
while True:
    current_guess_index = len(game.guess_history) + 1
    word = player.prompt_word()

    player.on_guess_feedback(*game.make_guess(word))

    print(render_game(game))

    if game.is_win:
        print("You guessed the word!")
        break

    if game.is_done:
        print(f"Ran out of guesses.")
        break

print(f"The secret word was {bold(game.secret_word)}.")
