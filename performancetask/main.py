from __future__ import annotations
import pygame
from pygame import draw, display, time, key
from random import randint
from math import sin, cos, pi, sqrt
import json


class Vec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_angle(cls, angle: float, magnitude: float = 1):
        return cls(x=cos(angle) * magnitude, y=sin(angle) * magnitude)

    @property
    def t(self) -> tuple[float, float]:
        return (self.x, self.y)

    @property
    def sqrmagnitude(self) -> float:
        return self.x**2 + self.y**2

    @property
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def draw(self, surface: pygame.Surface):
        draw.circle(surface, "green", (self.x, self.y), 2)

    def cross(self, other: Vec2) -> float:
        return self.x * other.y - self.y * other.x

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"( {self.x}, {self.y} )"

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float) -> Vec2:
        return Vec2(self.x * other, self.y * other)


class Line:
    def __init__(self, start_pos: Vec2, end_pos: Vec2) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos

    @classmethod
    def from_ray(cls, origin: Vec2, angle: float, distance: float = 2048):
        return cls(
            start_pos=origin, end_pos=origin + Vec2(cos(angle), sin(angle)) * distance
        )

    def find_intersection_with_line(self, other: Line) -> None | Vec2:
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
        self, origin: Vec2, angle: float, max_distance: float = 2048
    ) -> None | Vec2:
        return self.find_intersection_with_line(
            self.from_ray(origin, angle, max_distance)
        )

    def draw(self, surface: pygame.Surface):
        draw.line(surface, "red", self.start_pos.t, self.end_pos.t)


class World:
    def __init__(self, path: str) -> None:
        with open(path, "r") as world_file:
            world_info: dict = json.load(world_file)

            if not isinstance(world_info, dict):
                raise
            if world_info.get("is_world", False) == False:
                raise

            self.name = world_info.get("name", "Unknown")
            self.points: list[Vec2] = [
                Vec2(p["x"], p["y"]) for p in world_info.get("points", [])
            ]
            self.lines: list[Line] = []

            for point, other_point in zip(self.points, self.points[1:]):
                print(point, other_point)
                self.lines.append(Line(point, other_point))

    def raycast(
        self, origin: Vec2, angle: float, max_distance: float = 2048
    ) -> tuple[Vec2, float] | None:
        ray_line = Line.from_ray(origin, angle, max_distance)

        record_point = None
        record_dist = max_distance

        for other_line in self.lines:
            hit_point = ray_line.find_intersection_with_line(other_line)
            if hit_point == None:
                continue
            dist = (hit_point - origin).magnitude
            if dist > record_dist:
                continue
            record_dist = dist
            record_point = hit_point

        if record_point == None:
            return None

        return (record_point, record_dist)

    def draw(self, surface: pygame.Surface):
        draw.lines(surface, "red", False, [p.t for p in self.points])


class Player:
    def __init__(self) -> None:
        self.pos: Vec2 = Vec2(0, 0)
        self.velocity: Vec2 = Vec2(0, 0)
        self.angle: float = 0
        self.dangle: float = 0

    def impulse(self, speed: Vec2):
        self.velocity += speed

    def angle_impulse(self, speed: float):
        self.dangle += speed

    def update(self, dt: float):
        self.pos += self.velocity * dt
        self.angle += self.dangle * dt
        self.velocity *= 0.9
        self.dangle *= 0.9

    def draw(self, surface: pygame.Surface):
        forward = Vec2(cos(self.angle), sin(self.angle))
        right = Vec2(cos(self.angle + pi / 2), sin(self.angle + pi / 2))

        draw.polygon(
            surface,
            "yellow",
            [
                (self.pos + forward * 8).t,
                (self.pos + right * 3).t,
                (self.pos - right * 3).t,
            ],
        )
        draw.line(surface, "green", self.pos.t, (self.pos + self.velocity).t)


current_world = World("world.json")
current_player = Player()
current_player.pos = Vec2(100, 100)

pygame.init()

screen_surface = pygame.display.set_mode((900, 900))


def draw_screen():
    screen_surface.fill("black")
    current_world.draw(screen_surface)
    current_player.draw(screen_surface)

    result = current_world.raycast(current_player.pos, current_player.angle, 2048)

    if result:
        draw.line(screen_surface, "pink", current_player.pos.t, result[0].t)
        draw.circle(screen_surface, "pink", result[0].t, 4)

    display.flip()


def process_input():
    pressed = key.get_pressed()

    if pressed[pygame.K_a]:
        current_player.angle_impulse(-0.5)
    if pressed[pygame.K_d]:
        current_player.angle_impulse(0.5)
    if pressed[pygame.K_w]:
        current_player.impulse(Vec2.from_angle(current_player.angle, 40))
    if pressed[pygame.K_s]:
        current_player.impulse(Vec2.from_angle(current_player.angle, -40))


def update_world(dt: float):
    current_player.update(dt)


dt = 1
clock = time.Clock()
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    process_input()
    update_world(dt)
    draw_screen()

    dt = clock.tick(60) / 1000

pygame.quit()
