from tkinter import Tk, Frame
from random import randrange

root = Tk()
root.title("phys")
root.geometry(f"900x900")

class Entity:
	def update(self) -> None:
		...

class Box(Entity):
	def __init__(self, master=root) -> None:
		self._root = master

		size = randrange(10, 60)
		self.width = size
		self.height = size

		self.pos_x = 0
		self.pos_y = -90
		self.vel_x = randrange(0, 500) / 100
		self.vel_y = randrange(0, 500) / 100
		self._frame = Frame(master=root, width=self.width, height=self.height, bg="red",borderwidth=1)
	
	def update(self) -> None:
		if self.pos_y < -self._root.winfo_height() + self.height:
			self.vel_y *= -1
		
		if self.pos_x < 0 or self.pos_x > self._root.winfo_width() - self.width:
			self.vel_x *= -1

		self.pos_x += self.vel_x
		self.pos_y += self.vel_y

		self.vel_y -= 0.1

		self._frame.place(x=self.pos_x, y=-self.pos_y)

ENTITIES: list[Entity] = []

def update_entities():
	for entity in ENTITIES:
		entity.update()

ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())
ENTITIES.append(Box())

def update_main():
	update_entities()

	root.after(16, update_main)

update_main()

root.mainloop()