from pyansi import bold
from modules.formatting import format_guess
from modules.guesser import WordleGuesser
from modules.dictionary import DICTIONARY
from wordle import LocalWordleGame
from random import choice


def render_game(game: LocalWordleGame) -> str:
    output = "\x1b[2J\x1b[H\n"

    for guess_index, guess in enumerate(game.guess_history):
        word, word_validity = guess

        output += f"{guess_index + 1} > {format_guess(word, word_validity)}\n"

    output += "\n"

    return output


game = LocalWordleGame(choice(DICTIONARY), max_guesses=6)
player = WordleGuesser(game, DICTIONARY)

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
