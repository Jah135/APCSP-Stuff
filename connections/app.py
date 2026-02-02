from tkinter import Tk


class ConnectionsApp:
	def __init__(self) -> None:
		root = Tk()

		self.root = root
	
	def start(self):
		self.root.mainloop()