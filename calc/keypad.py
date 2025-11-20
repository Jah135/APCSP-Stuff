from tkinter import Misc, Frame, Button
from enums import CalculatorOperation, KeypadCommand
from typing import Callable

# LAYOUT
# Text, Row, Column, Command, Command Arguments (as a tuple)

KEYPAD = [
	("1", 0, 0, KeypadCommand.WriteNumber, 1),
	("2", 1, 0, KeypadCommand.WriteNumber, 2),
	("3", 2, 0, KeypadCommand.WriteNumber, 3),
	("4", 0, 1, KeypadCommand.WriteNumber, 4),
	("5", 1, 1, KeypadCommand.WriteNumber, 5),
	("6", 2, 1, KeypadCommand.WriteNumber, 6),
	("7", 0, 2, KeypadCommand.WriteNumber, 7),
	("8", 1, 2, KeypadCommand.WriteNumber, 8),
	("9", 2, 2, KeypadCommand.WriteNumber, 9),
	("0", 0, 3, KeypadCommand.WriteNumber, 0),

	("+", 3, 0, KeypadCommand.SetOperation, CalculatorOperation.Add),
	("-", 3, 1, KeypadCommand.SetOperation, CalculatorOperation.Subtract),
	("*", 3, 2, KeypadCommand.SetOperation, CalculatorOperation.Multiply),
	("/", 3, 3, KeypadCommand.SetOperation, CalculatorOperation.Divide),

	("=", 2, 3, KeypadCommand.Evaluate, ()),
	("CLR", 1, 3, KeypadCommand.Clear, ())
]

class Keypad(Frame):
	def __init__(self, master: Misc, keypad_callback: Callable, **kwargs):
		super().__init__(master=master, **kwargs)

		for button_info in KEYPAD:
			text, col, row, c_id, c_args = button_info

			keypad_button_command = lambda c_id=c_id, c_args=c_args: keypad_callback(c_id, c_args)

			button = Button(master=self, relief="groove", text=text, padx=-1, width=4, height=1, borderwidth=2, command=keypad_button_command)
			button.grid(column=col, row=row)
			master.bind(text, lambda _, f=keypad_button_command: f())