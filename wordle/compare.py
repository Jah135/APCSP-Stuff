from modules.auto import WordleGuesser, WordleGame, DICTIONARY
from random import choice

game = WordleGame()
guesser = WordleGuesser(game)

for word in DICTIONARY:
    game.secret_word = choice(DICTIONARY)

    while not game.is_over:
        guesser.make_guess()
    
    if not game.is_won:
        print(f"FAILED: {word}")
    else:
        print(f"PASSED: {word}")

    game.reset()
    guesser.reset()
