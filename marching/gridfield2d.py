"""
D---0---A
|       |
3       1
|       |
C---2---B

A = 1
B = 2
C = 4
D = 8
"""

VERTEX_VEC_OFFSETS: list[tuple[float, float]] = [
    (0.5, 0),
    (1, 0.5),
    (0.5, 1),
    (0, 0.5),
]
CONTOUR_VERTEX_INDICES: list[list[int]] = [
    [],  # 0
    [0, 1],  # 1
    [1, 2],  # 2
    [0, 2],  # 3
    [2, 3],  # 4
    [0, 1, 2, 3],  # 5
    [1, 3],  # 6
    [0, 3],  # 7
    [0, 3],  # 8
    [1, 3],  # 9
    [1, 2, 0, 3],  # 10
    [2, 3],  # 11
    [0, 2],  # 12
    [1, 2],  # 13
    [0, 1],  # 14
    [],  # 15
]


class GridField2D:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.values: list[int] = [0] * (width * height)

    def set_point(self, x: int, y: int, value: int):
        if x > self.width or y > self.height:
            return

        self.values[x + y * self.width] = value

    def sample_point(self, x: int, y: int):
        if x > self.width - 1 or y > self.height - 1:
            return 0

        return self.values[x + y * self.width]

    def sample_cell_state(self, x: int, y: int, threshold: int = 0):
        d = self.sample_point(x, y) > threshold
        a = self.sample_point(x + 1, y) > threshold
        c = self.sample_point(x, y + 1) > threshold
        b = self.sample_point(x + 1, y + 1) > threshold

        return a | (b * 2) | (c * 4) | (d * 8)

    def get_contour_vertex_indices(self, x: int, y: int, threshold: int = 0):
        return CONTOUR_VERTEX_INDICES[self.sample_cell_state(x, y, threshold)]

    def get_contour_vertex_offsets(self, x: int, y: int, threshold: int = 0):
        return [
            VERTEX_VEC_OFFSETS[index]
            for index in self.get_contour_vertex_indices(x, y, threshold)
        ]
