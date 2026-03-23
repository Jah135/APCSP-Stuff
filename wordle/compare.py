from modules.guesser import WordleGuesser, WordleGame, DICTIONARY

game = WordleGame()
guesser = WordleGuesser(game)

for word in DICTIONARY:
    game.secret_word = word

    while not game.is_over:
        guesser.prompt_word()
    
    if not game.is_won:
        print(f"FAILED: {word}")
        break
    else:
        print(f"PASSED: {word}")

    game.reset()
    guesser.reset()
