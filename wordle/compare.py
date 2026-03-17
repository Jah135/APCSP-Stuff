from modules.guesser import WordleGuesser, WordleGame, DICTIONARY
from random import choice

game = WordleGame()
guesser = WordleGuesser(game)

while True:
    while not game.is_over:
        guesser.make_guess()
    
    if not game.is_won:
        break

    game.reset()
    game.secret_word = choice(DICTIONARY)
    guesser.reset()

print("failed to guess word for", game.secret_word)
    