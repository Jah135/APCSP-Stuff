from __future__ import annotations
from math import sqrt, cos, sin, acos
import pygame


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
    def square_magnitude(self) -> float:
        return self.x**2 + self.y**2

    @property
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    @property
    def unit(self) -> Vec2:
        return self / self.magnitude

    def distance_from(self, other: Vec2) -> float:
        return (self - other).magnitude

    def square_distance_from(self, other: Vec2) -> float:
        return (self - other).square_magnitude

    def direction_towards(self, other: Vec2) -> Vec2:
        return (self - other).unit

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, "green", (self.x, self.y), 2)

    def cross(self, other: Vec2) -> float:
        return self.x * other.y - self.y * other.x

    def dot(self, other: Vec2) -> float:
        return self.x * other.x + self.y * other.y

    def angle(self, other: Vec2) -> float:
        return acos(self.dot(other))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"( {self.x}, {self.y} )"

    def __neg__(self):
        return self * -1

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __truediv__(self, other: float | Vec2):
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        return Vec2(self.x / other, self.y / other)

    def __mul__(self, other: float | Vec2) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return Vec2(self.x * other, self.y * other)
