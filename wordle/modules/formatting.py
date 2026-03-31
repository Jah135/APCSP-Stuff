from typing import Literal
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


TABLE_TOP_LEFT = "╭"
TABLE_TOP_RIGHT = "╮"
TABLE_BOTTOM_LEFT = "╰"
TABLE_BOTTOM_RIGHT = "╯"
TABLE_VERTICAL_SEP = "│"
TABLE_HORIZONTAL_SEP = "─"
TABLE_HORIZONTAL_SEP_THIN = "╌"
TABLE_COLUMN_TOP = "┬"
TABLE_COLUMN_BOTTOM = "┴"
TABLE_A_JUNCTION = "┼"
TABLE_R_JUNCTION = "├"
TABLE_L_JUNCTION = "┤"


def render_table(
    row_labels: list[str],
    col_labels: list[str],
    data_colrow: list[list[str]],
    *,
    with_borders=True,
    sep_headers=True,
    align_just: Literal["left"] | Literal["center"] | Literal["right"] = "center"
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
            if align_just == "left":
                formatted = value.ljust(width)
            elif align_just == "center":
                formatted = value.center(width)
            elif align_just == "right":
                formatted = value.rjust(width)
            row.append(formatted)
        line = TABLE_VERTICAL_SEP.join(row)
        if with_borders:
            line = TABLE_VERTICAL_SEP + line + TABLE_VERTICAL_SEP
        lines.append(line)
        if sep_headers and row_index == 0:
            sep_line = TABLE_A_JUNCTION.join(
                TABLE_HORIZONTAL_SEP_THIN * width for width in column_widths
            )
            if with_borders:
                sep_line = TABLE_R_JUNCTION + sep_line + TABLE_L_JUNCTION
            lines.append(sep_line)

    if with_borders:
        lines.insert(
            0,
            TABLE_TOP_LEFT
            + TABLE_COLUMN_TOP.join(
                TABLE_HORIZONTAL_SEP * width for width in column_widths
            )
            + TABLE_TOP_RIGHT,
        )
        lines.append(
            TABLE_BOTTOM_LEFT
            + TABLE_COLUMN_BOTTOM.join(
                TABLE_HORIZONTAL_SEP * width for width in column_widths
            )
            + TABLE_BOTTOM_RIGHT
        )
    return "\n".join(lines)
