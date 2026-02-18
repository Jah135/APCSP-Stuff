from __future__ import annotations
from typing import TYPE_CHECKING
from tkinter import Misc, Button
from math import sqrt, floor

if TYPE_CHECKING:
	from .app import ConnectionsApp

MINIMUM_BUTTON_SIZE = 11

BUTTON_SELECTED_BG = "#727272"
BUTTON_BG = "#d1d1d1"
BUTTON_PRESS_BG = "#414141"

class ConnectionsButton:
	def __init__(self, root: Misc, index: int, app: ConnectionsApp) -> None:
		base_root = sqrt(len(app.items))

		max_columns = floor(base_root)

		column = index % max_columns
		row = index // max_columns

		button = Button(root, text="na", font="TkFixedFont", relief="groove",command=lambda: app.select(index))
		button.grid(column=column, row=row, padx=2, pady=2)
		
		self._app = app
		self._index = index

		self.button = button
		self.update()
	
	def update(self):
		text = self._app.items[self._index]
		is_selected = self._index in self._app.selected

		self.button.configure(
			text=text.upper().center(MINIMUM_BUTTON_SIZE),
			bg=BUTTON_SELECTED_BG if is_selected else BUTTON_BG,
			activebackground=BUTTON_PRESS_BG
		)