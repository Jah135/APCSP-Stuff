from tkinter import Tk, Frame
from random import randrange
from typing import Self

root = Tk()
root.title("phys")
root.geometry(f"900x900")

class Entity:
	def update(self) -> None:
		...

class Vec2:
	def __init__(self, x: float = 0, y: float = 0) -> None:
		self.x = x
		self.y = y

	def scale(self, factor: float):
		self.x *= factor
		self.y *= factor

		return self
	def add(self, other: Self):
		self.x += other.x
		self.y += other.y

		return self
	def sub(self, other: Self):
		self.x -= other.x
		self.y -= other.y

		return self
	def negate(self):
		self.x = -self.x
		self.y = -self.y
		return self
	
	def __add__(self, other: Self):
		return Vec2(self.x + other.x, self.y + other.y)
	def __sub__(self, other: Self):
		return Vec2(self.x - other.x, self.y - other.y)
	def __mul__(self, other):
		if isinstance(other, float):
			return Vec2(self.x * other, self.y * other)
		elif isinstance(other, Vec2):
			return Vec2(self.x * other.x, self.y * other.y)
		
		raise Exception("Invalid __mul__ value")

class Box(Entity):
	def __init__(self, master=root) -> None:
		self._root = master

		self.size = Vec2(1, 1).scale(randrange(10, 60))
		self.pos = Vec2()
		self.vel = Vec2()

		self._frame = Frame(master=root, width=self.size.x, height=self.size.y, bg="red",borderwidth=1)
	
	def update(self) -> None:
		size = self.size

		if self.pos.y < -self._root.winfo_height() + size.y:
			self.vel.y *= -1
		
		if self.pos.x < 0 or self.pos.x > self._root.winfo_width() - size.x:
			self.vel.x *= -1

		dif = Vec2(100, 0) - self.pos 

		self.pos.add(self.vel)
		# self.vel.y -= 0.1
		self.vel.sub(dif.scale(0.001))

		self._frame.place(x=self.pos.x, y=self.pos.y)

ENTITIES: list[Entity] = []

def update_entities():
	for entity in ENTITIES:
		entity.update()

ENTITIES.append(Box())

def update_main():
	update_entities()

	root.after(16, update_main)

update_main()

root.mainloop()