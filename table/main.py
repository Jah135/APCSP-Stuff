def render_table(
    row_labels: list[str],
    col_labels: list[str],
    data_cr: list[list[str]],
    *,
    sep: str = " | ",
    column_widths: list[int] | None = None
) -> str:
    all_columns = [
        ["", *row_labels],
        *([label, *data_cr[index]] for index, label in enumerate(col_labels)),
    ]
    column_widths = column_widths or [
        max(len(str(x)) for x in column) for column in all_columns
    ]

    lines = []

    for row_index in range(len(row_labels) + 1):
        row = []

        for width, col in zip(column_widths, all_columns):
            try:
                value = str(col[row_index])
            except:
                value = ""
            row.append(value[:width].center(width))
        lines.append(sep + sep.join(row) + sep)
    return "\n".join(lines)


print(
    render_table(
        ["row 1", "row 2", "row 30"],
        ["col 1", "col 2"],
        [["a", "b", "z"], ["c", "d", "e"]],
        sep="|",
        column_widths=[16, 15, 15],
    )
)
