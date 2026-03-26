from __future__ import annotations

import pygame
from pygame import draw, display, event, key, time
from pygame import (
    Rect,
    Surface,
    K_w as KEY_W,
    K_s as KEY_S,
    K_UP as KEY_UP,
    K_DOWN as KEY_DOWN,
)

from random import randint

PLAYER_SPEED = 500  # pixels per second
SCREEN_SIZE = (1000, 500)


def clamp(x: float, min_x: float, max_x: float) -> float:
    return min(max(x, min_x), max_x)


ENTITIES: list[Entity] = []


class Entity:
    def __init__(self) -> None:
        ENTITIES.append(self)

    def update(self, dt: float): ...
    def draw(self): ...

    def remove(self):
        ENTITIES.remove(self)


class Player(Entity):
    width = 10
    height = 100

    def __init__(self, surface: Surface) -> None:
        super().__init__()
        self.surface = surface
        self.x = 0
        self.y = 0
        self.dy = 0

    def update(self, dt: float):
        self.y = clamp(self.y + self.dy, 0, SCREEN_SIZE[1] - self.height)

    def draw(self):
        draw.rect(
            self.surface,
            "white",
            Rect(
                self.x,
                self.y,
                self.width,
                self.height,
            ),
        )


class HumanPlayer(Player):
    def __init__(self, surface: Surface, up_key: int, down_key: int) -> None:
        super().__init__(surface)
        self.up_key = up_key
        self.down_key = down_key

    def update(self, dt: float):
        pressed_keys = key.get_pressed()

        self.dy = 0

        if pressed_keys[self.up_key]:
            self.dy = -PLAYER_SPEED * dt
        if pressed_keys[self.down_key]:
            self.dy = PLAYER_SPEED * dt

        return super().update(dt)


class Ball(Entity):
    radius = 6

    def __init__(
        self,
        surface: Surface,
        position: tuple[int, int] = (0, 0),
        velocity: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__()
        self.surface = surface
        self.x = position[0]
        self.y = position[1]
        self.dx = velocity[0]
        self.dy = velocity[1]

    def update(self, dt: float):
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_SIZE[1]:
            self.dy *= -1

        for other in ENTITIES:
            if not isinstance(other, Player):
                continue
            if (
                self.x - self.radius <= other.x + other.width
                and self.x + self.radius >= other.x
                and self.y - self.radius <= other.y + other.height
                and self.y + self.radius >= other.y
            ):
                self.dx *= -1
                # self.dy += (other.dy / dt) // 2

        self.x += round(self.dx * dt)
        self.y += round(self.dy * dt)

    def draw(self):
        draw.circle(self.surface, "white", (self.x, self.y), self.radius)


pygame.init()

active_screen = display.set_mode(SCREEN_SIZE)
display.set_caption("Pong")


ball = Ball(
    active_screen,
    position=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
    velocity=(randint(190, 270), randint(80, 190)),
)
player1 = HumanPlayer(active_screen, KEY_W, KEY_S)
player1.x = 20
player1.y = 100

player2 = HumanPlayer(active_screen, KEY_UP, KEY_DOWN)
player2.x = SCREEN_SIZE[0] - 30


def draw_scene():
    active_screen.fill("black")
    for entity in ENTITIES:
        entity.draw()
    display.flip()


def update_scene(dt: float):
    for entity in ENTITIES:
        entity.update(dt)


clock = time.Clock()

running = True

while running:
    for e in event.get():
        if e.type == pygame.QUIT:
            running = False

    update_scene(clock.tick(120) / 1000)
    draw_scene()

pygame.quit()
