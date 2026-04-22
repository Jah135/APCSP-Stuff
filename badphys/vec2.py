from __future__ import annotations
from math import sqrt, cos, sin, acos, pi
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
        """A tuple representation of this vector."""
        return (self.x, self.y)

    @property
    def square_magnitude(self) -> float:
        """The square magnitude of this vector."""
        return self.x**2 + self.y**2

    @property
    def magnitude(self) -> float:
        """The magnitude of this vector."""
        return sqrt(self.x**2 + self.y**2)

    @property
    def unit(self) -> Vec2:
        """A `Vec2` with the same direction as this `Vec2`, with a magnitude of 1."""
        return self / self.magnitude

    def rotated(self, angle: float) -> Vec2:
        """Returns a version of this `Vec2` rotated around the origin by the specified amount."""
        return Vec2(
            self.x * cos(angle) + self.y * cos(angle + pi / 2),
            self.x * sin(angle) + self.y * sin(angle + pi / 2),
        )

    def distance_from(self, point: Vec2) -> float:
        """Returns the distance from this `Vec2` to the specified point."""
        return (self - point).magnitude

    def square_distance_from(self, point: Vec2) -> float:
        """Returns the square distance from this `Vec2` to the specified point."""
        return (self - point).square_magnitude

    def direction_towards(self, point: Vec2) -> Vec2:
        """Returns a unit `Vec2` pointing from this `Vec2` to the specified point."""
        return (self - point).unit

    def cross(self, vector: Vec2) -> float:
        """Returns the cross product of this `Vec2` and the specified `Vec2`."""
        return self.x * vector.y - self.y * vector.x

    def dot(self, vector: Vec2) -> float:
        """Returns the dot product of this `Vec2` and the specified `Vec2`."""
        return self.x * vector.x + self.y * vector.y

    def angle(self, vector: Vec2) -> float:
        """Returns the arccos of the dot product of this `Vec2` and the specified `Vec2`."""
        return acos(self.dot(vector))

    def debug_draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, "green", (self.x, self.y), 2)

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
