from modules.formatting import format_guess
from modules.game import WordleGame, DICTIONARY, choice
from modules.guesser import WordleGuesser
from modules.player import WordlePlayer

target_word = choice(DICTIONARY)

def format_games(human_game: WordleGame, bot_game: WordleGame) -> str:
    lines = []

    for index, guess in enumerate(human_game.guesses):
        lines.append(f"{index + 1} > {format_guess(*guess)}")
    
    for index, guess in enumerate(bot_game.guesses):
        word, validity = guess
        display_word = word if human_game.is_over else "?" * len(word)
        lines[index] += f"  {format_guess(display_word, validity)}"

    return "\n".join(lines)

bot_game = WordleGame(secret_word=target_word)
bot_player = WordleGuesser(bot_game)

human_game = WordleGame(secret_word=target_word)
human_player = WordlePlayer(human_game)

while not human_game.is_over:
    if not bot_game.is_over:
        bot_player.make_guess(None if len(bot_game.guesses) > 0 else choice(DICTIONARY))

    human_player.make_guess()

    print(format_games(human_game, bot_game))

if human_game.is_won == bot_game.is_won and len(human_game.guesses) == len(bot_game.guesses):
    print("You tied with the bot!")
elif human_game.is_won and len(human_game.guesses) <= len(bot_game.guesses):
    print("You won!")
else:
    print("You lost to the bot!")

print(f"The word was {target_word}")