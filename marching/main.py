import pygame
import pygame.draw as draw
from random import randint

from game import Game
from gridfield2d import GridField2D

CELL_SIZE = 10

pygame.font.init()
font = pygame.font.Font(None, 20)


class TestGame(Game):
    window_width = 500
    window_height = 500
    target_framerate = 1

    def __init__(self) -> None:
        super().__init__()

        field = GridField2D(50, 50)

        for i in range(field.width * field.height):
            field.values[i] = randint(0, 4)

        self.field = field

    def on_draw(self, out: pygame.Surface):
        out.fill("black")

        for x in range(self.field.width):
            for y in range(self.field.height):
                value = self.field.sample_point(x, y)

                base_x = x * CELL_SIZE
                base_y = y * CELL_SIZE

                points = [
                    (base_x + offset[0] * CELL_SIZE, base_y + offset[1] * CELL_SIZE)
                    for offset in self.field.get_contour_vertex_offsets(x, y, 3)
                ]
                point_groups = [
                    (points[index], points[index + 1])
                    for index in range(0, len(points), 2)
                ]

                for group in point_groups:
                    draw.line(out, "red", group[0], group[1])

    # def on_update(self, dt: float): ...


game = TestGame()
game.start()
