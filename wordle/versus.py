from modules.formatting import format_guess, bold
from modules.game import WordleGame, DICTIONARY, choice
from modules.guesser import WordleGuesser
from modules.player import WordlePlayer, HumanWordlePlayer
from modules.names import get_first_name

MAX_GUESSES = 6
TARGET_WORD = choice(DICTIONARY)
DISPLAY_GUESS_WIDTH = len(TARGET_WORD) * 3
BOT_COUNT = 8

VersusPlayer = tuple[WordlePlayer, WordleGame, str]


def render_games(
    games: list[WordleGame], labels: list[str], hidden_games: set[WordleGame]
) -> str:
    lines = []

    label_line = "    "

    for label in labels:
        label_line += label.capitalize().ljust(DISPLAY_GUESS_WIDTH + 2)

    lines.append(label_line)

    for index in range(max(len(game.guesses) for game in games)):
        line = f"{index + 1} > "
        for game in games:
            try:
                word, validity = game.guesses[index]
                display_word = "?" * len(TARGET_WORD) if game in hidden_games else word
                line += format_guess(display_word, validity) + "  "
            except:
                line += " " * DISPLAY_GUESS_WIDTH + "  "
        lines.append(line)

    return "\n".join(lines)


def get_placings(players: list[VersusPlayer]):
    scores: list[tuple[str, int]] = []

    for player in players:
        _, game, label = player
        score = MAX_GUESSES - len(game.guesses) + 20 if game.is_won else 0
        scores.append((label, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores


bot_players: list[VersusPlayer] = []

for _ in range(BOT_COUNT):
    bot_game = WordleGame(max_guesses=MAX_GUESSES, secret_word=TARGET_WORD)
    bot_player = WordleGuesser(bot_game)
    bot_players.append((bot_player, bot_game, get_first_name()))

human_game = WordleGame(max_guesses=MAX_GUESSES, secret_word=TARGET_WORD)
human_player = HumanWordlePlayer(len(TARGET_WORD))

print(
    f"\033[H\033[2J{bold("Versus Wordle")}\nGuess the secret {bold(str(len(TARGET_WORD)))} letter word before the bots!\n"
)

bot_games = [bot[1] for bot in bot_players]
all_games = [human_game, *bot_games]
all_players: list[VersusPlayer] = [(human_player, human_game, "you"), *bot_players]

while not (human_game.is_over and all(game.is_over for game in bot_games)):
    for bot in bot_players:
        bot_player, bot_game, label = bot
        if not bot_game.is_over:
            bot_player.on_guess_feedback(
                *bot_game.make_guess(
                    bot_player.prompt_word()
                    if len(bot_game.guesses) > 0
                    else choice(DICTIONARY)
                )
            )
            print(f"{label} has guessed")

    if not human_game.is_over:
        human_player.on_guess_feedback(
            *human_game.make_guess(human_player.prompt_word("Your guess"))
        )

    print(
        "\x1b[2J\x1b[H\n"
        + render_games(
            all_games,
            [player[2] for player in all_players],
            set() if human_game.is_over else set(bot_games),
        )
    )


print(f"The word was {bold(TARGET_WORD)}.")

placings = get_placings(all_players)

for place_index, player in enumerate(placings):
    print(f"#{place_index + 1}. {player[0].capitalize()}")
