from __future__ import annotations
import json
import pygame
from pygame import font, draw, display, time, key
from math import pi, degrees

from vec2 import Vec2
from line import Line


pygame.init()

DEBUG_FONT = font.Font(None, size=20)


class World:
    def __init__(self, path: str) -> None:
        with open(path, "r") as world_file:
            world_info: dict = json.load(world_file)

            if not isinstance(world_info, dict):
                raise
            if world_info.get("is_world", False) == False:
                raise

            self.name = world_info.get("name", "Unknown")

            groups: list[list[dict]] = world_info.get("points", [])

            point_groups: list[list[Vec2]] = [
                [Vec2(p["x"], p["y"]) for p in group] for group in groups
            ]
            tags_groups: list[list[set[str]]] = [
                [set(p.get("tags", [])) for p in group] for group in groups
            ]
            attributes_groups: list[list[dict]] = [
                [p.get("attributes", {}) for p in group] for group in groups
            ]

            all_lines: list[Line] = []

            self.point_groups = point_groups
            self.tags_groups = tags_groups
            self.attributes_groups = attributes_groups
            self.all_lines = all_lines

            for points, tags, attributes in zip(
                point_groups, tags_groups, attributes_groups
            ):
                for point, other_point, line_tags, line_attributes in zip(
                    points, points[1:], tags, attributes
                ):
                    all_lines.append(
                        Line(
                            start_pos=point,
                            end_pos=other_point,
                            tags=line_tags,
                            attributes=line_attributes,
                        )
                    )

    def raycast(
        self,
        origin: Vec2,
        direction: Vec2,
        max_distance: float = 2048,
        ignore_tags: set[str] = {"ignore"},
    ) -> tuple[Vec2, float, Line] | None:
        ray_line = Line(origin, origin + direction, {"ray"})

        record_point = None
        record_line = None
        record_dist = max_distance

        for other_line in self.all_lines:
            if bool(ignore_tags & other_line.tags):
                continue

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
        for line in self.all_lines:
            col = line.attributes.get("color", "red")
            draw.line(
                surface,
                col,
                line.start_position.t,
                line.end_position.t,
            )


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
        premove_collision_result = WORLD.raycast(
            self.position,
            self.velocity * dt,
            ignore_tags={"noclip"},
        )

        if premove_collision_result:
            _, _, line = premove_collision_result
            normal = line.get_normal_for_point(self.position)
            self.velocity -= normal * normal.dot(self.velocity)
            self.colliding_with = line

            postmove_collision_result = WORLD.raycast(
                self.position, self.velocity * dt, ignore_tags={"noclip"}
            )

            if postmove_collision_result:
                pos, _, _ = postmove_collision_result
                self.position = pos - normal
            else:
                self.position += self.velocity * dt
        else:
            self.colliding_with = None
            self.position += self.velocity * dt

        self.angle += self.dangle * dt

        self.velocity *= 0.6
        self.dangle *= 0.6

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
        draw.arc(
            surface,
            "purple",
            pygame.Rect(self.position.x, self.position.y, 10, 10),
            self.angle,
            self.angle + self.dangle,
        )
        draw.line(surface, "green", self.position.t, (self.position + self.velocity).t)
        draw.circle(surface, "purple", (self.position + self.velocity * dt).t, 3)


WORLD = World("world.json")
PLAYER = Player()
PLAYER.position = Vec2(100, 100)


SCREEN = pygame.display.set_mode((900, 900))
fov = 90


def draw_screen():
    SCREEN.fill("black")
    WORLD.draw(SCREEN)
    PLAYER.draw(SCREEN)

    line = WORLD.all_lines[2]
    p = line.start_position

    ang = (p - PLAYER.position).unit.angle(PLAYER.look_vector)

    SCREEN.blit(DEBUG_FONT.render(str(degrees(ang)), True, "white"), p.t)

    draw.circle(SCREEN, "yellow", p.t, 3)

    # ordered_lines = world.all_lines[:]
    # ordered_lines.sort(
    #     key=lambda line: player.position.distance_from(
    #         line.find_closest_point_on_line(player.position)
    #     ),
    #     reverse=True,
    # )

    # for index, line in enumerate(ordered_lines):
    #     start_dot = -player.position.direction_towards(line.start_position).dot(
    #         player.look_vector
    #     )

    #     if start_dot < 0:
    #         continue

    #     start_screen_pos = Vec2(450, 450) - (Vec2(450, 0) * (1 - start_dot))

    #     draw.circle(screen, "green", start_screen_pos.t, 4)
    #     screen.blit(
    #         debug_font.render(str(1 - start_dot), True, "white"), line.start_position.t
    #     )
    #     screen.blit(debug_font.render(str(index), True, "white"), start_screen_pos.t)

    display.flip()


def process_input():
    pressed = key.get_pressed()

    if pressed[pygame.K_a]:
        PLAYER.angle_impulse(-1.5)
    if pressed[pygame.K_d]:
        PLAYER.angle_impulse(1.5)
    if pressed[pygame.K_w]:
        PLAYER.impulse(Vec2.from_angle(PLAYER.angle, 100))
    if pressed[pygame.K_s]:
        PLAYER.impulse(Vec2.from_angle(PLAYER.angle, -100))


def update_world(dt: float):
    PLAYER.update(dt)


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
