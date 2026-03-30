from __future__ import annotations
import pygame
from pygame import draw, display, time, key
from random import randint
from math import sin, cos, pi
import json


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface):
        draw.circle(surface, "green", (self.x, self.y), 2)

    def cross(self, other: Point) -> float:
        return self.x * other.y - self.y * other.x

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"( {self.x}, {self.y} )"

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float) -> Point:
        return Point(self.x * other, self.y * other)


class Line:
    def __init__(self, start_pos: Point, end_pos: Point) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos

    @classmethod
    def from_ray(cls, origin: Point, angle: float, distance: float = 2048):
        return cls(
            start_pos=origin, end_pos=origin + Point(cos(angle), sin(angle)) * distance
        )

    def find_intersection_with_line(self, other: Line) -> None | Point:
        p = self.start_pos
        r = self.end_pos - p  # p + r = self endpos

        q = other.start_pos
        s = other.end_pos - q  # q + s = other endpos

        dif = q - p
        den = r.cross(s)
        if den == 0:
            den = 0.000001
        t = dif.cross(s) / den
        u = dif.cross(r) / den

        if t < 0 or t > 1 or u < 0 or u > 1:
            return None

        return p + (r * t)

    def find_intersection_with_ray(
        self, origin: Point, angle: float, max_distance: float = 2048
    ) -> None | Point:
        return self.find_intersection_with_line(
            self.from_ray(origin, angle, max_distance)
        )

    def draw(self, surface: pygame.Surface):
        draw.line(surface, "red", self.start_pos.as_tuple(), self.end_pos.as_tuple())


class World:
    def __init__(self, path: str) -> None:
        with open(path, "r") as world_file:
            world_info: dict = json.load(world_file)

            if not isinstance(world_info, dict):
                raise
            if world_info.get("is_world", False) == False:
                raise

            self.name = world_info.get("name", "Unknown")
            self.points: list[Point] = [
                Point(p["x"], p["y"]) for p in world_info.get("points", [])
            ]
            self.lines: list[Line] = []

            for point, other_point in zip(self.points, self.points[1:]):
                print(point, other_point)
                self.lines.append(Line(point, other_point))

    def draw(self, surface: pygame.Surface):
        draw.lines(surface, "red", False, [p.as_tuple() for p in self.points])


class Player:
    def __init__(self) -> None:
        self.pos: Point = Point(0, 0)
        self.angle: float = 0

    def move(self, speed: float, dt: float):
        dir = Point(cos(self.angle), sin(self.angle))
        self.pos += dir * speed * dt

    def turn(self, speed: float, dt: float):
        self.angle += speed * dt

    def draw(self, surface: pygame.Surface):
        forward = Point(cos(self.angle), sin(self.angle))
        right = Point(cos(self.angle + pi / 2), sin(self.angle + pi / 2))

        draw.polygon(
            surface,
            "yellow",
            [
                (self.pos + forward * 8).as_tuple(),
                (self.pos + right * 3).as_tuple(),
                (self.pos - right * 3).as_tuple(),
            ],
        )


current_world = World("world.json")
current_player = Player()
current_player.pos = Point(100, 100)

pygame.init()

screen_surface = pygame.display.set_mode((900, 900))


def draw_screen():
    screen_surface.fill("black")
    current_world.draw(screen_surface)
    current_player.draw(screen_surface)
    display.flip()


def process_input(dt: float):
    pressed = key.get_pressed()

    if pressed[pygame.K_a]:
        current_player.turn(-2, dt)
    if pressed[pygame.K_d]:
        current_player.turn(2, dt)
    if pressed[pygame.K_w]:
        current_player.move(50, dt)


dt = 1
clock = time.Clock()
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    process_input(dt)
    draw_screen()

    dt = clock.tick(60) / 1000

pygame.quit()
