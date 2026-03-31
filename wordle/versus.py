from modules.formatting import bold, render_table
from modules.guesser import WordleGuesser
from modules.player import WordlePlayer, LocalWordlePlayer
from modules.names import get_first_name
from modules.dictionary import DICTIONARY
from wordle import LocalWordleGame
from wordle.formatting import format_guess
from random import choice

MAX_GUESSES = 6
TARGET_WORD = choice(DICTIONARY)
BOT_COUNT = 8

VersusPlayer = tuple[WordlePlayer, LocalWordleGame, str]


def render_games(
    games: list[LocalWordleGame],
    game_labels: list[str],
    hidden_games: set[LocalWordleGame],
) -> str:
    return render_table(
        [
            f" Guess {index + 1} "
            for index in range(max(len(game.guess_history) for game in games))
        ],
        [label.capitalize() for label in game_labels],
        [
            [
                format_guess(
                    (word if game not in hidden_games else "?" * len(word), validity)
                )
                for (word, validity) in game.guess_history
            ]
            for game in games
        ],
        with_borders=True,
        sep_headers=True,
    )


def get_placings(players: list[VersusPlayer]):
    scores: list[tuple[str, int]] = []

    for player in players:
        _, game, label = player
        score = MAX_GUESSES - len(game.guess_history) + 20 if game.is_won else 0
        scores.append((label, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


bot_players: list[VersusPlayer] = []

for _ in range(BOT_COUNT):
    bot_game = LocalWordleGame(max_guesses=MAX_GUESSES, secret_word=TARGET_WORD)
    bot_player = WordleGuesser(bot_game, DICTIONARY)
    bot_players.append((bot_player, bot_game, get_first_name()))

human_game = LocalWordleGame(max_guesses=MAX_GUESSES, secret_word=TARGET_WORD)
human_player = LocalWordlePlayer(len(TARGET_WORD), DICTIONARY)

print(
    f"\033[H\033[2J{bold("Versus Wordle")}\nGuess the secret {bold(str(len(TARGET_WORD)))} letter word before the bots!\n"
)

bot_games = [bot[1] for bot in bot_players]
all_games = [human_game, *bot_games]
all_players: list[VersusPlayer] = [(human_player, human_game, "you"), *bot_players]

while not (human_game.is_done and all(game.is_done for game in bot_games)):
    for bot in bot_players:
        bot_player, bot_game, label = bot
        if not bot_game.is_done:
            bot_player.on_guess_feedback(
                *bot_game.make_guess(
                    bot_player.prompt_word()
                    if len(bot_game.guess_history) > 0
                    else choice(DICTIONARY)
                )
            )

    if not human_game.is_done:
        human_player.on_guess_feedback(
            *human_game.make_guess(human_player.prompt_word())
        )

    print(
        "\x1b[2J\x1b[H\n"
        + render_games(
            all_games,
            [player[2] for player in all_players],
            set() if human_game.is_done else set(bot_games),
        )
    )


print(f"The word was {bold(TARGET_WORD)}.")

placings = get_placings(all_players)

for place_index, player in enumerate(placings):
    print(f"#{place_index + 1}. {player[0].capitalize()}")
