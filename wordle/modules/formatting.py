from pyansi import AnsiStyle, PaletteColor, Palette, bold, remove_ansi
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


KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")


def render_keyboard(validity: dict[str, LetterValidity]):
    output = ""

    for i, row in enumerate(KEYBOARD_ROWS):
        output += (
            "  " * i
            + ("".join(format_letter(letter, validity.get(letter)) for letter in row))
            + "\n"
        )

    return output


def render_table(
    row_labels: list[str],
    col_labels: list[str],
    data_colrow: list[list[str]],
    *,
    sep: str = " | ",
) -> str:
    all_columns = [
        ["", *row_labels],
        *([label, *data_colrow[index]] for index, label in enumerate(col_labels)),
    ]
    column_widths = [
        max(len(remove_ansi(str(x))) for x in column) for column in all_columns
    ]

    lines = []

    for row_index in range(len(row_labels) + 1):
        row = []

        for width, col in zip(column_widths, all_columns):
            try:
                value = str(col[row_index])
            except:
                value = ""
            row.append(value.center(width))
        lines.append(sep + sep.join(row) + sep)
    return "\n".join(lines)
