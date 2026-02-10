from tkinter import Tk, Button, Misc
from random import shuffle

MINIMUM_BUTTON_SIZE = 11

class ConnectionsButton:
	def __init__(self, root: Misc, items: list[str], index: int) -> None:
		self._items = items
		self._index = index

		button = Button(root, text="na", font="TkFixedFont", relief="groove")
		button.grid(column=index // 4, row=index % 4, ipadx=2, ipady=2)
		
		self.button = button

		self.update()
	
	def update(self):
		text = self._items[self._index]

		self.button.configure(text=text.upper().center(MINIMUM_BUTTON_SIZE))

class ConnectionsApp:
	def __init__(self) -> None:
		window = Tk()
		window.title("Connections")

		self.window = window
	
	def shuffle(self):
		shuffle(self.all_items)

		for button in self.buttons:
			button.update()
	
	def start(self, groups: list[tuple[str, list[str]]]):
		self.groups = groups
		self.buttons = []
		self.all_items = []

		window = self.window

		for group in groups:
			for item in group[1]:
				self.all_items.append(item)

		for index, item in enumerate(self.all_items):
			self.buttons.append(ConnectionsButton(window, self.all_items, index))

		self.shuffle()

		window.mainloop()