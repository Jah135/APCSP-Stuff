from __future__ import annotations
from vec2 import Vec2
import pygame


class Line:
    def __init__(self, start_pos: Vec2, end_pos: Vec2) -> None:
        self.start_position = start_pos
        self.end_position = end_pos

    @classmethod
    def from_ray(cls, origin: Vec2, angle: float, distance: float = 2048):
        return cls(start_pos=origin, end_pos=origin + Vec2.from_angle(angle) * distance)

    @property
    def parallel_vector(self) -> Vec2:
        return (self.end_position - self.start_position).unit

    @property
    def perpendicular_vector(self) -> Vec2:
        parallel = self.parallel_vector
        return Vec2(-parallel.y, parallel.x)

    @property
    def center(self) -> Vec2:
        return (self.start_position + self.end_position) / 2

    @property
    def length(self) -> float:
        return (self.start_position - self.end_position).magnitude

    @property
    def square_length(self) -> float:
        return (self.start_position - self.end_position).square_magnitude

    def get_side(self, point: Vec2) -> float:
        to_point = (self.start_position - point).unit
        prod = self.perpendicular_vector.dot(to_point)

        return -1 if prod < 0 else 0 if prod == 0 else 1

    def find_intersection_with_line(self, other: Line) -> Vec2 | None:
        p = self.start_position
        r = self.end_position - p  # p + r = self endpos

        q = other.start_position
        s = other.end_position - q  # q + s = other endpos

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
    ) -> Vec2 | None:
        return self.find_intersection_with_line(
            self.from_ray(origin, angle, max_distance)
        )

    def find_closest_point_on_line(self, point: Vec2):
        l = self.square_length

        if l == 0:
            return self.start_position

        u = point - self.start_position
        v = self.end_position - self.start_position
        t = min(max(u.dot(v) / l, 0), 1)

        return self.start_position + v * t

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface, "red", self.start_position.t, self.end_position.t)
