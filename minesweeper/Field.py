# imports :)
from random import Random
from pyansi import AnsiStyle, Palette, PaletteColor
from typing import Callable
import kernels

# FIELD STATES
CLOSED = 0b00
OPEN = 0b01
MINE = 0b10
FLAGGED = 0b100

# 0               000
# ^-> FLAG STATE  ^^^-> FIELD STATE

MAX_SAFETY_ATTEMPTS = 8

MINE_KERNEL = kernels.NORMAL

DANGER_STYLES = [
    AnsiStyle(fg=Palette(PaletteColor.BrightBlue)),
    AnsiStyle(fg=Palette(PaletteColor.BrightGreen)),
    AnsiStyle(fg=Palette(PaletteColor.BrightRed)),
    AnsiStyle(fg=Palette(PaletteColor.BrightMagenta)),
    AnsiStyle(fg=Palette(PaletteColor.BrightCyan)),
    AnsiStyle(fg=Palette(PaletteColor.Yellow)),
    AnsiStyle(fg=Palette(PaletteColor.Red)),
    AnsiStyle(fg=Palette(PaletteColor.BrightBlack)),
]
FLAG_STYLE = AnsiStyle(
    fg=Palette(PaletteColor.BrightYellow), bg=Palette(PaletteColor.Red)
)
CLOSED_STYLE = AnsiStyle(
    fg=Palette(PaletteColor.BrightBlack), bg=Palette(PaletteColor.BrightBlack)
)
MINE_STYLE = AnsiStyle(
    fg=Palette(PaletteColor.Black), bg=Palette(PaletteColor.BrightRed)
)
HIGHLIGHT_STYLE = AnsiStyle(
    bg=Palette(PaletteColor.BrightWhite), fg=Palette(PaletteColor.Black)
)
KERNEL_STYLE = AnsiStyle(
    bg=Palette(PaletteColor.BrightYellow), fg=Palette(PaletteColor.Black)
)


# Returns field type
def extract_type(state: int) -> int:
    return state & ~FLAGGED


# Returns whether the state is flagged
def extract_flagged(state: int) -> bool:
    return state & FLAGGED != 0


class Field:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self._field = bytearray(width * height)

        self.has_exploded = False
        self.first_move = True

        self.width = width
        self.height = height

        self._rand = Random(seed)

    def _read_field(self, index: int) -> int:
        return self._field[index] & ~FLAGGED

    def read_field(self, x: int, y: int) -> int:
        return self._read_field(self.to_index(x, y))

    def _write_field(self, index: int, new_state: int):
        self._field[index] = self._field[index] & FLAGGED | new_state

    def write_field(self, x: int, y: int, state: int):
        self._write_field(self.to_index(x, y), state)

    def _read_flag(self, index: int) -> bool:
        return self._field[index] & FLAGGED != 0

    def read_flag(self, x: int, y: int) -> bool:
        return self._read_flag(self.to_index(x, y))

    def _write_flag(self, index: int, is_flagged: bool):
        if is_flagged:
            self._field[index] |= FLAGGED
        else:
            self._field[index] &= ~FLAGGED

    def write_flag(self, x: int, y: int, is_flagged: bool):
        self._write_flag(self.to_index(x, y), is_flagged)

    def within_bounds(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def to_index(self, x: int, y: int) -> int:
        return self.width * y + x

    def place_mine(self):
        while True:
            index = self._rand.randint(0, self.width * self.height - 1)

            if self._read_field(index) != MINE:
                self._write_field(index, MINE)
                break

    def place_mines(self, count: int):
        for _ in range(count):
            self.place_mine()

    def get_flag_count(self) -> int:
        count = 0

        for state in self._field:
            if extract_flagged(state):
                count += 1

        return count

    def get_state_count(self, state: int) -> int:
        count = 0

        for field_state in self._field:
            if extract_type(field_state) == state:
                count += 1

        return count

    def is_win_state(self):
        if self.has_exploded:
            return False

        all_flagged = True

        for state in self._field:
            if extract_type(state) == MINE and not extract_flagged(state):
                all_flagged = False
                break

        return all_flagged and self.get_state_count(CLOSED) == 0

    def run_kernel(
        self, x: int, y: int, applier: Callable[[int, int, int], None]
    ) -> None:
        for offset_x, offset_y in MINE_KERNEL:
            target_x, target_y = x + offset_x, y + offset_y

            if not self.within_bounds(target_x, target_y):
                continue

            index = self.to_index(target_x, target_y)

            applier(index, target_x, target_y)

    def count_kernel(
        self, x: int, y: int, predicate: Callable[[int, int, int], bool]
    ) -> int:
        count = 0

        for offset_x, offset_y in MINE_KERNEL:
            check_x, check_y = x + offset_x, y + offset_y

            if not self.within_bounds(check_x, check_y):
                continue

            index = self.to_index(check_x, check_y)

            if not predicate(index, check_x, check_y):
                continue

            count += 1

        return count

    def get_kernel_state_count(self, x: int, y: int, state: int) -> int:
        return self.count_kernel(
            x, y, lambda index, *_: self._read_field(index) == state
        )

    def get_kernel_flag_count(self, x: int, y: int) -> int:
        return self.count_kernel(x, y, lambda index, *_: self._read_flag(index))

    def ensure_safety(self, x: int, y: int):
        is_totally_safe = False

        attempts = 0

        while not is_totally_safe:
            if attempts > MAX_SAFETY_ATTEMPTS:
                print("MAXIMUM SAFETY ATTEMPTS EXCEEDED!")
                break

            attempts += 1
            is_totally_safe = True

            for off_x, off_y in [(0, 0), *MINE_KERNEL]:
                target_x, target_y = x + off_x, y + off_y

                if not self.within_bounds(target_x, target_y):
                    continue

                if self.read_field(target_x, target_y) == MINE:
                    is_totally_safe = False
                    self.write_field(target_x, target_y, CLOSED)

    def player_open_cell(self, x: int, y: int, do_recurse: bool = True):
        if not self.within_bounds(x, y):
            return

        index = self.to_index(x, y)

        if self._read_flag(index):
            return

        # ensure safety
        if self.first_move:
            self.first_move = False
            self.ensure_safety(x, y)

        # die on mine
        if self._read_field(index) == MINE:
            self.has_exploded = True

            return

        danger = self.get_kernel_state_count(x, y, MINE)

        if self._read_field(index) == OPEN:
            # CHORDING
            if do_recurse and danger == self.get_kernel_flag_count(x, y):
                for off_x, off_y in MINE_KERNEL:
                    # pass
                    self.player_open_cell(x + off_x, y + off_y, do_recurse=False)

                return

            return

        self._write_field(index, OPEN)

        if danger == 0:  # open neighboring cells
            self.run_kernel(x, y, lambda _, x, y: self.player_open_cell(x, y, False))

        return

    def player_flag_cell(self, x: int, y: int, do_recurse: bool = True):
        if not self.within_bounds(x, y):
            return

        if self.read_field(x, y) == OPEN:
            # CHORDING
            if do_recurse:
                closed_count = self.get_kernel_state_count(x, y, CLOSED)
                mine_count = self.get_kernel_state_count(x, y, MINE)

                if closed_count == 0 and mine_count > 0:
                    self.run_kernel(
                        x,
                        y,
                        lambda _, tx, ty: (
                            self.player_flag_cell(tx, ty, do_recurse=False)
                            if not self.read_flag(tx, ty)
                            else None
                        ),
                    )

            return

        self.write_flag(x, y, not self.read_flag(x, y))

        return


def render_field(
    field: Field,
    cursor_position: tuple[int, int],
    show_kernel: bool = False,
    show_mines: bool = False,
) -> str:
    output = ""

    highlight_indices = [field.to_index(*cursor_position)]
    kernel_indices = []

    if show_kernel:
        for off_x, off_y in MINE_KERNEL:
            check_x, check_y = (
                cursor_position[0] + off_x,
                cursor_position[1] + off_y,
            )

            if not field.within_bounds(check_x, check_y):
                continue

            kernel_indices.append(field.to_index(check_x, check_y))

    should_show_mines = show_mines or field.has_exploded

    for y in range(field.height):
        for x in range(field.width):
            index = y * field.width + x

            state = field.read_field(x, y)
            is_flagged = field.read_flag(x, y)
            is_highlighted = index in highlight_indices
            is_kernel = index in kernel_indices

            px_style = None
            px = ""

            if state == OPEN:
                danger = field.get_kernel_state_count(x, y, MINE)

                if danger == 0:
                    px = ". "
                else:
                    px = f"{danger} "

                    if not is_highlighted:
                        px_style = DANGER_STYLES[danger - 1]
            else:
                if is_flagged:
                    px = "P "
                    px_style = FLAG_STYLE
                else:
                    if state == MINE and should_show_mines:
                        px = "X "
                        px_style = MINE_STYLE
                    else:
                        px = "? "
                        px_style = CLOSED_STYLE

            if is_highlighted:
                px_style = HIGHLIGHT_STYLE

            if is_kernel:
                px_style = KERNEL_STYLE

            if px_style != None:
                px = px_style.apply_with_reset(px)

            output += px

        output += "\n"

    return output
