from pyansi import AnsiStyle, PaletteColor, Palette, bold
from wordle import LocalWordleGame, LetterValidity

CORRECT_STYLE = AnsiStyle(
    bg=Palette(PaletteColor.BrightGreen), fg=Palette(PaletteColor.Black)
)
INCORRECT_STYLE = AnsiStyle(
    bg=Palette(PaletteColor.BrightBlack), fg=Palette(PaletteColor.Black)
)
EXISTS_STYLE = AnsiStyle(
    bg=Palette(PaletteColor.Yellow), fg=Palette(PaletteColor.Black)
)
NEUTRAL_STYLE = AnsiStyle(
    bg=Palette(PaletteColor.White), fg=Palette(PaletteColor.Black)
)


def format_letter(char: str, validity: LetterValidity | None = None) -> str:
    display = f" {char.upper()} "
    if validity == None:
        return NEUTRAL_STYLE.apply_with_reset(display)
    elif validity == LetterValidity.Correct:
        return CORRECT_STYLE.apply_with_reset(display)
    elif validity == LetterValidity.Exists:
        return EXISTS_STYLE.apply_with_reset(display)
    return INCORRECT_STYLE.apply_with_reset(display)


def format_guess(guess: str, guess_validity: list[LetterValidity]) -> str:
    return "".join(
        format_letter(char, validity) for char, validity in zip(guess, guess_validity)
    )


def render_game(game: LocalWordleGame) -> str:
    output = "\x1b[2J\x1b[H\n"

    for guess_index, guess in enumerate(game.guess_history):
        word, word_validity = guess

        output += f"{guess_index + 1} > {format_guess(word, word_validity)}\n"

    output += "\n"

    return output


KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")


def render_keyboard(validity: dict[str, LetterValidity]):
    output = ""

    for row in KEYBOARD_ROWS:
        output += (
            "".join(format_letter(letter, validity.get(letter)) for letter in row)
        ) + "\n"

    return output
