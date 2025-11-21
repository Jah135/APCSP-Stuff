from world import World

class Particle:
    @staticmethod
    def update(world: World, x: int, y: int):
        ...
    
    @staticmethod
    def render(x: int, y: int) -> str:
        return ". "
