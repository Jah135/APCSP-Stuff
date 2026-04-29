from pygame.surface import Surface
import pygame.draw as draw

from game import Game

pos = (100, 100)
vel = (50, -130)


class TestGame(Game):
    window_width = 500
    window_height = 500
    target_framerate = -1

    def on_draw(self, out: Surface):
        out.fill("black")

        draw.circle(out, "pink", pos, 2)
        draw.line(out, "blue", pos, (pos[0] + vel[0], pos[1] + vel[1]))

    def on_update(self, dt: float):
        global pos, vel

        pos = (pos[0] + vel[0] * dt, pos[1] + vel[1] * dt)
        vel = (vel[0], vel[1] + 60 * dt)


game = TestGame()
game.start()
