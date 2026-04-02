from __future__ import annotations
import json
import pygame
from pygame import Font, draw, display, time, key
from math import pi, radians

from vec2 import Vec2
from line import Line


class World:
    def __init__(self, path: str) -> None:
        with open(path, "r") as world_file:
            world_info: dict = json.load(world_file)

            if not isinstance(world_info, dict):
                raise
            if world_info.get("is_world", False) == False:
                raise

            self.name = world_info.get("name", "Unknown")
            self.point_groups: list[list[Vec2]] = [
                [Vec2(p["x"], p["y"]) for p in group]
                for group in world_info.get("points", [])
            ]
            self.lines: list[Line] = []

            for group in self.point_groups:
                for point, other_point in zip(group, group[1:]):
                    self.lines.append(Line(point, other_point))

    def raycast(
        self, origin: Vec2, direction: Vec2, max_distance: float = 2048
    ) -> tuple[Vec2, float, Line] | None:
        ray_line = Line(origin, origin + direction)

        record_point = None
        record_line = None
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
            record_line = other_line

        if record_point == None or record_line == None:
            return None

        return (record_point, record_dist, record_line)

    def draw(self, surface: pygame.Surface):
        for group in self.point_groups:
            draw.lines(surface, "red", False, [p.t for p in group])


class Player:
    def __init__(self) -> None:
        self.position: Vec2 = Vec2(0, 0)
        self.velocity: Vec2 = Vec2(0, 0)
        self.angle: float = 0
        self.dangle: float = 0
        self.colliding_with: Line | None = None

    @property
    def look_vector(self) -> Vec2:
        return Vec2.from_angle(self.angle)

    @property
    def right_vector(self) -> Vec2:
        return Vec2.from_angle(self.angle + pi / 2)

    def impulse(self, speed: Vec2):
        self.velocity += speed

    def angle_impulse(self, speed: float):
        self.dangle += speed

    def update(self, dt: float):
        collision_result = world.raycast(self.position, self.velocity * dt)

        if collision_result:
            pos, _, line = collision_result
            normal = line.perpendicular_vector * line.get_side(self.position)
            self.position = pos - normal
            self.colliding_with = line
        else:
            self.position += self.velocity * dt
            self.colliding_with = None
            # self.velocity = Vec2(0, 0)

        self.angle += self.dangle * dt
        self.velocity *= 0.9
        self.dangle *= 0.9

    def draw(self, surface: pygame.Surface):
        forward = self.look_vector
        right = self.right_vector

        draw.lines(
            surface,
            "yellow",
            True,
            [
                (self.position + forward * 8).t,
                (self.position + right * 3).t,
                (self.position - right * 3).t,
            ],
        )
        draw.line(surface, "green", self.position.t, (self.position + self.velocity).t)


world = World("world.json")
player = Player()
player.position = Vec2(100, 100)

pygame.init()

screen = pygame.display.set_mode((900, 900))
fov = 90

debug_font = Font(size=20)


def draw_screen():
    screen.fill("black")
    world.draw(screen)
    player.draw(screen)

    if player.colliding_with:
        draw.line(
            screen,
            "blue",
            player.colliding_with.start_position.t,
            player.colliding_with.end_position.t,
        )

    ordered_lines = world.lines[:]
    ordered_lines.sort(
        key=lambda line: player.position.distance_from(
            line.find_closest_point_on_line(player.position)
        ),
        reverse=True,
    )

    for index, line in enumerate(ordered_lines):
        start_dot = -player.position.direction_towards(line.start_position).dot(
            player.look_vector
        )

        if start_dot < 0:
            continue

        start_screen_pos = Vec2(450, 450) - (Vec2(450, 0) * (1 - start_dot))

        draw.circle(screen, "green", start_screen_pos.t, 4)
        screen.blit(
            debug_font.render(str(1 - start_dot), True, "white"), line.start_position.t
        )
        screen.blit(debug_font.render(str(index), True, "white"), start_screen_pos.t)

    display.flip()


def process_input():
    pressed = key.get_pressed()

    if pressed[pygame.K_a]:
        player.angle_impulse(-0.5)
    if pressed[pygame.K_d]:
        player.angle_impulse(0.5)
    if pressed[pygame.K_w]:
        player.impulse(Vec2.from_angle(player.angle, 40))
    if pressed[pygame.K_s]:
        player.impulse(Vec2.from_angle(player.angle, -40))


def update_world(dt: float):
    player.update(dt)


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
