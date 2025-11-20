class BufferedList:
	def __init__(self, size: int, default) -> None:
		self._current = [default] * size
		self._buffer = self._current.copy()

		self._default = default
	
	def write_at(self, index: int, value):
		self._buffer[index] = value

	def read_at(self, index: int):
		return self._current[index]
	def read_buffer_at(self, index: int):
		return self._buffer[index]
	
	def consume_buffer(self):
		self._current, self._buffer = self._buffer, self._current

		# reset buffer, there's probably a better way to do this
		for index in range(len(self._buffer)):
			self._buffer[index] = self._default

class World:
	def __init__(self, width: int, height: int, default) -> None:
		self.width = width
		self.height = height

		self._data = BufferedList(width * height, default)
	
	def is_in_bounds(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def _get_index(self, x: int, y: int) -> int:
		return x + y * self.width
	
	def read(self, x: int, y: int):
		if not self.is_in_bounds(x, y):
			return None

		return self._data.read_at(self._get_index(x, y))
	def write(self, x: int, y: int, value):
		if not self.is_in_bounds(x, y):
			return

		self._data.write_at(self._get_index(x, y), value)
	def apply(self):
		self._data.consume_buffer()

class Particle:
	@staticmethod
	def update(world: World, x: int, y: int):
		...
class Air(Particle):
	...
class Sand(Particle):
	@staticmethod
	def update(world: World, x: int, y: int):
		if world.read(x, y + 1) == Air:
			world.write(x, y, Air)
			world.write(x, y + 1, Sand)

def update_world(world: World):
	for y in range(world.height):
		for x in range(world.width):
			part: Particle | None = world.read(x, y)

			if part != None:
				part.update(world, x, y)

def render_world(world: World) -> str:
	output = ""

	for y in range(world.height):
		line = ""

		for x in range(world.width):
			line += "#"
		
		output += line + "\n"


	return output

world = World(5, 5, Air)

print(render_world(world))