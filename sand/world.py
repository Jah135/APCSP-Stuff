class BufferedList:
	def __init__(self, size: int, default) -> None:
		self.data = [default] * size
		self.buffer = self.data.copy()

		self._size = size
		self._default_value = default
	
	def write(self, index: int, value):
		self.buffer[index] = value
	def read(self, index: int):
		return self.data[index]
	def read_buffer(self, index: int):
		return self.buffer[index]

	def consume_buffer(self):
		self.data, self.buffer = self.buffer, self.data
		
		for index in range(self._size):
			self.buffer[index] = self._default_value
			
class World:
	def __init__(self, width: int, height: int, default) -> None:
		self.width = width
		self.height = height

		self._data = BufferedList(width * height, default)
	
	def _get_index(self, x: int, y: int) -> int:
		return x + y * self.width
	
	def exists(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def read(self, x: int, y: int):
		if not self.exists(x, y):
			return None

		return self._data.read(self._get_index(x, y))
	def write(self, x: int, y: int, value):
		if not self.exists(x, y):
			return

		self._data.write(self._get_index(x, y), value)
	def swap(self, from_x: int, from_y: int, to_x: int, to_y: int):
		if not self.exists(from_x, from_y) or not self.exists(to_x, to_y):
			return
		
		from_value = self.read(from_x, from_y)
		to_value = self.read(to_x, to_y)

		self.write(to_x, to_y, from_value)
		self.write(from_x, from_y, to_value)
	def identity(self, x: int, y: int):
		self.write(x, y, self.read(x, y))

	def apply_changes(self):
		self._data.consume_buffer()
