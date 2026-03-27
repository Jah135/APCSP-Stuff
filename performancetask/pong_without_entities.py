from __future__ import annotations
import pygame
from pygame import draw, display, time, mouse
from random import randint
from math import sin, cos


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def cross(self, other: Point) -> float:
        return self.x * other.y - self.y * other.x

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

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

    # def find_intersection_with_ray(self, ray_origin: tuple[int, int], angle: float):
    def find_intersection_with_line(self, other: Line) -> None | Point:
        p = self.start_pos
        r = self.end_pos - p  # p + r = self endpos

        q = other.start_pos
        s = other.end_pos - q  # q + s = other endpos

        qp_dif = q - p
        den = r.cross(s)
        t = qp_dif.cross(s) / den
        u = qp_dif.cross(r) / den

        if t < 0 or t > 1 or u < 0 or u > 1:
            return None

        return p + (r * t)

    def draw(self, surface: pygame.Surface):
        draw.line(surface, "red", self.start_pos.as_tuple(), self.end_pos.as_tuple())


pygame.init()

screen_surface = pygame.display.set_mode((500, 500))

line1 = Line(Point(10, 10), Point(50, 50))
line2 = Line(Point(50, 100), Point(50, 10))


def draw_screen():
    screen_surface.fill("black")
    line1.draw(screen_surface)
    line2.draw(screen_surface)
    point = line1.find_intersection_with_line(line2)

    if point != None:
        draw.circle(screen_surface, "green", point.as_tuple(), 3)

    display.flip()


clock = time.Clock()
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    line1.end_pos = Point(*mouse.get_pos())

    draw_screen()

    clock.tick(60)

pygame.quit()
