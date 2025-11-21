from pyansi import AnsiStyle, Palette, PaletteColor

from .particle import Particle, World
from .air import Air

SAND_RENDER = AnsiStyle(bg=Palette(PaletteColor.Yellow)).apply_with_reset("  ")

class Sand(Particle):
    @staticmethod
    def update(world: World, x: int, y: int):
        if world.read(x, y + 1) == Air:
            world.swap(x, y, x, y + 1)
        elif world.read(x + 1, y + 1) == Air:
            world.swap(x, y, x + 1, y + 1)
        elif world.read(x - 1, y + 1) == Air:
            world.swap(x, y, x - 1, y + 1)
        else:
            world.identity(x, y)
    
    @staticmethod
    def render(x: int, y: int) -> str:
        return SAND_RENDER