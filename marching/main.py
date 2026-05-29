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

        field = GridField2D(20, 20)

        self.field = field

    def on_draw(self, out: pygame.Surface):
        out.fill("black")

        for x in range(self.field.width):
            for y in range(self.field.height):

                base_x = x * CELL_SIZE
                base_y = y * CELL_SIZE

                lines = [
                    tuple(
                        (base_x + point[0] * CELL_SIZE, base_y + point[1] * CELL_SIZE)
                        for point in group
                    )
                    for group in self.field.get_vertex_contour_offsets(x, y)
                ]

                for group in lines:
                    draw.line(out, "red", group[0], group[1])

                value = self.field.sample_point(x, y)

                draw.circle(out, (int(value), 0, 0), (base_x, base_y), 3)


game = TestGame()
game.start()
