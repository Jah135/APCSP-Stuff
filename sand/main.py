from time import sleep

from world import World
from particles.particle import Particle
from particles.sand import Sand
from particles.air import Air

def update_world(world: World):
	for y in range(world.height):
		use_y = world.height - y - 1
		for x in range(world.width):
			particle: Particle | None = world.read(x, use_y)

			if particle != None:
				particle.update(world, x, use_y)
	world.apply_changes()
def render_world(world: World) -> str:
	output = ""

	for y in range(world.height):
		line = ""

		for x in range(world.width):
			particle: Particle | None = world.read(x, y)

			if particle != None:
				line += particle.render(x, y)
				
		
		output += line + "\n"


	return output

world = World(11, 11, Air)

while True:
	world.write(0, 0, Sand)
	world.write(5, 0, Sand)
	update_world(world)
	print(render_world(world))
	sleep(0.2)