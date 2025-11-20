from time import sleep

def isa(cls, super) -> bool:
	if cls == None:
		return False
	
	return issubclass(cls, super)

class World:
	def __init__(self, width: int, height: int, default) -> None:
		self.width = width
		self.height = height

		# self._data = BufferedList(width * height, default)
		self._data = [default] * width * height
	
	def _get_index(self, x: int, y: int) -> int:
		return x + y * self.width
	
	def exists(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def read(self, x: int, y: int):
		if not self.exists(x, y):
			return None

		return self._data[self._get_index(x, y)]
	def write(self, x: int, y: int, value):
		if not self.exists(x, y):
			return

		self._data[self._get_index(x, y)] = value

class Solid:
	...
class Replacable:
	...

class Particle:
	@staticmethod
	def update(world: World, x: int, y: int):
		...
	
	@staticmethod
	def render() -> str:
		return ". "
	
class Air(Particle, Replacable):
	...
class Sand(Particle, Solid):
	@staticmethod
	def update(world: World, x: int, y: int):
		world.write(x, y, Air)

		if isa(world.read(x, y + 1), Replacable):
			world.write(x, y + 1, Sand)
		elif isa(world.read(x + 1, y + 1), Replacable):
			world.write(x + 1, y + 1, Sand)
		elif isa(world.read(x - 1, y + 1), Replacable):
			world.write(x - 1, y + 1, Sand)
		else:
			world.write(x, y, Sand)
	
	@staticmethod
	def render():
		return "# "
class Water(Particle, Solid, Replacable):
	@staticmethod
	def update(world: World, x: int, y: int):
		world.write(x, y, Air)

		if not isa(world.read(x, y + 1), Solid) and world.exists(x, y + 1):
			world.write(x, y + 1, Water)
		elif not isa(world.read(x + 1, y + 1), Solid) and world.exists(x + 1, y + 1):
			world.write(x + 1, y + 1, Water)
		elif not isa(world.read(x - 1, y + 1), Solid) and world.exists(x - 1, y + 1):
			world.write(x - 1, y + 1, Water)
		elif not isa(world.read(x + 1, y), Solid) and world.exists(x + 1, y):
			world.write(x + 1, y, Water)
		elif not isa(world.read(x - 1, y), Solid) and world.exists(x - 1, y):
			world.write(x - 1, y, Water)
		else:
			world.write(x, y, Water)
	@staticmethod
	def render():
		return "~ "

def update_world(world: World):
	for y in range(world.height):
		use_y = world.height - y - 1
		for x in range(world.width):
			part: Particle | None = world.read(x, use_y)

			if part != None:
				part.update(world, x, use_y)
def render_world(world: World) -> str:
	output = ""

	for y in range(world.height):
		line = ""

		for x in range(world.width):
			part: Particle | None = world.read(x, y)

			if part == None:
				line += ". "
			else:
				line += part.render()
				
		
		output += line + "\n"


	return output

world = World(11, 11, Air)

world.write(5, 0, Water)

while True:
	update_world(world)
	print(render_world(world))
	sleep(0.2)