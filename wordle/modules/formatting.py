from pyansi import bold, remove_ansi
from wordle import LetterValidity
from wordle.formatting import format_letter


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
    with_borders=True,
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
        line = sep.join(row)
        if with_borders:
            line = sep + line + sep
        lines.append(line)
    return "\n".join(lines)
