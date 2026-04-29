from __future__ import annotations
from vec2 import Vec2
from math import atan
import pygame


class Line:
    def __init__(
        self,
        start_pos: Vec2,
        end_pos: Vec2,
        tags: set[str] = set(),
        attributes: dict = {},
    ) -> None:
        self.start_position = start_pos
        self.end_position = end_pos

        self.tags = tags
        self.attributes = attributes

    @classmethod
    def from_ray(
        cls,
        origin: Vec2,
        angle: float,
        distance: float = 2048,
        tags: set[str] = set(),
        attributes: dict = {},
    ):
        return cls(
            start_pos=origin,
            end_pos=origin + Vec2.from_angle(angle) * distance,
            tags=tags,
            attributes=attributes,
        )

    @property
    def parallel_vector(self) -> Vec2:
        """A `Vec2` describing a direction that is parrellel to this line."""
        return (self.end_position - self.start_position).unit

    @property
    def perpendicular_vector(self) -> Vec2:
        """A `Vec2` describing a direction that is perpendicular, or tangent, to this line."""
        parallel = self.parallel_vector
        return Vec2(-parallel.y, parallel.x)

    @property
    def midpoint(self) -> Vec2:
        """The midpoint/center of this line."""
        return (self.start_position + self.end_position) / 2

    @property
    def length(self) -> float:
        """The distance between the start and end position of this line."""
        return self.start_position.distance_from(self.end_position)

    @property
    def square_length(self) -> float:
        """The square length of this line."""
        return self.start_position.square_distance_from(self.end_position)

    @property
    def slope(self) -> float:
        d = self.end_position - self.start_position

        return 1e9 if d.x == 0 else d.y / d.x

    @property
    def angle(self) -> float:
        return atan(self.slope)

    def get_normal_towards_point(self, point: Vec2) -> Vec2:
        """Returns a `Vec2` describing the normal of the surface the specified point is closest to."""
        return self.perpendicular_vector * self.get_is_above_sign(point)

    def get_is_above_sign(self, point: Vec2) -> float:
        """Returns an integer representing whether the point is above the line (1), on the line (0) or below the line (-1)"""
        y_at_x = self.start_position.y + (point.x - self.start_position.x) * self.slope

        return -1 if y_at_x < point.y else 0 if y_at_x == point.y else 1

    def find_intersection_with_line(self, other: Line) -> Vec2 | None:
        """Returns a `Vec2` if this line segment and the specified line segment intersect, otherwise returns `None`."""
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
        """Returns a `Vec2` if this line segment and the specified ray intersect, otherwise returns `None`."""
        return self.find_intersection_with_line(
            self.from_ray(origin, angle, max_distance)
        )

    def find_closest_point_on_line(self, point: Vec2):
        """Returns the closest point on this line segment to the specified point."""
        l = self.square_length

        if l == 0:
            return self.start_position

        pd = point - self.start_position
        sd = self.end_position - self.start_position
        t = min(max(pd.dot(sd) / l, 0), 1)

        return self.start_position + sd * t

    def draw(self, surface: pygame.Surface):
        pygame.draw.line(surface, "red", self.start_position.tup, self.end_position.tup)
