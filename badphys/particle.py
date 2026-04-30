from vec2 import Vec2
from pygame import draw, Surface


class Particle:
    def __init__(
        self, init_pos: Vec2 = Vec2(0, 0), init_vel: Vec2 = Vec2(0, 0)
    ) -> None:
        self.position = init_pos
        self.velocity = init_vel
        self.mass = 1
        self.locked = False

    def apply_force(self, force: Vec2):
        self.velocity += force / self.mass

    def update(self, dt: float):
        if self.locked:
            return

        self.position += self.velocity * dt

    def debug_display_to(self, surface: Surface):
        draw.circle(surface, "red", self.position.t, 3)
