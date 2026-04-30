import json
import pygame

from line import Line
from vec2 import Vec2


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
            pygame.draw.line(
                surface,
                col,
                line.start_position.t,
                line.end_position.t,
            )
