def render_table(
    row_labels: list[str],
    column_labels: list[str],
    data_cr: list[list[str]],
    sep: str = " | ",
) -> str:
    row_label_width = max(len(x) for x in row_labels)
    column_widths: list[int] = [
        max((len(column_labels[column_index]), max(len(x) for x in column_data)))
        for column_index, column_data in enumerate(data_cr)
    ]
    rows: list[str] = []

    column_label_row: list[str] = [" " * row_label_width]
    for column_width, column_label in zip(column_widths, column_labels):
        column_label_row.append(column_label.ljust(column_width))

    rows.append(sep.join(column_label_row))

    for row_index, row_label in enumerate(row_labels):
        row: list[str] = [row_label.ljust(row_label_width)]
        for column_width, column in zip(column_widths, data_cr):
            col = column[row_index]
            row.append(col.ljust(column_width))

        rows.append(sep.join(row))

    return "\n".join(rows)


print(
    render_table(
        ["first row", "second row"],
        ["first column", "second column"],
        [["a", "b"], ["c1", "d2 2"]],
        sep="  ",
    )
)
