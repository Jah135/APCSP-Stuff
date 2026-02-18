from tkinter import Tk
from random import shuffle
from button import ConnectionsButton

class ConnectionsApp:
	def __init__(self, groups: list[tuple[str, list[str]]]) -> None:
		self.groups = groups
		self.selected: list[int] = []
		self.buttons: list[ConnectionsButton] = []
		self.items: list[str] = []

		window = Tk()
		window.title("Connections")

		self.window = window
	
	def shuffle(self):
		shuffle(self.items)

		for button in self.buttons:
			button.update()
		
	def select(self, index: int):
		if index in self.selected:
			self.selected.remove(index)
		else:
			self.selected.append(index)
		
		button = self.buttons[index]
		button.update()
	
	def start(self):
		window = self.window

		for group in self.groups:
			for item in group[1]:
				self.items.append(item)

		for index, item in enumerate(self.items):
			self.buttons.append(ConnectionsButton(window, index, self))

		window.mainloop()

