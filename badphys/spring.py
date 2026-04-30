from particle import Particle
from vec2 import Vec2


class Spring:
    def __init__(
        self,
        particle_a: Particle,
        particle_b: Particle,
        target_length: float = 10,
        stiffness: float = 10,
        dampening: float = 1,
    ) -> None:
        self.a = particle_a
        self.b = particle_b

        self.target_length = target_length
        self.stiffness = stiffness
        self.dampening = dampening

        self.last_displacement = (self.a.position - self.b.position).magnitude

    def update(self, dt: float):
        delta = self.a.position - self.b.position

        direction = delta.unit

        displacement = self.target_length - delta.magnitude
        velocity = (self.last_displacement - displacement) / dt

        force_magnitude = displacement * self.stiffness - (velocity * self.dampening)

        self.a.apply_force(direction * force_magnitude / 2)
        self.b.apply_force(-direction * force_magnitude / 2)
