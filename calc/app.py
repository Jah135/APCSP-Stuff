from tkinter import Tk, Label
from enums import CalculatorOperation, KeypadCommand
from keypad import Keypad

class CalculatorApp:
	def __init__(self) -> None:
		root = Tk()
		root.geometry("150x150")
		root.resizable(False, False)

		display_label = Label(root, text="", justify="right", relief="groove", width=20, pady=1, padx=-1)
		display_label.pack(anchor="w", padx=2)

		keypad = Keypad(root, self._handle_command)
		keypad.pack(anchor="w", pady=1, padx=2)

		self.root = root
		self.display = display_label

		# operation related properties
		self.operation_mode = CalculatorOperation.Add

		self.input_buffer = ""
		self.register = 0
	
	def _handle_command(self, cmd: KeypadCommand, *args):
		if cmd == KeypadCommand.SetOperation:
			self.set_operation_mode(*args)
		elif cmd == KeypadCommand.WriteNumber:
			self.write_input_buffer(*args)
		elif cmd == KeypadCommand.Evaluate:
			self.evaluate_equation()
		elif cmd == KeypadCommand.Clear:
			self.input_buffer = ""
			self.register = 0
			self.set_display("0")
			self.operation_mode = CalculatorOperation.Add
	def set_display(self, text: str):
		self.display.configure(text=text)

	def set_operation_mode(self, operation_mode: CalculatorOperation):
		self.consume_input_buffer()
		self.operation_mode = operation_mode
		self.set_display("0")
	# Moves value from input buffer into register, returns the new register value
	def consume_input_buffer(self):
		try:
			self.register = int(self.input_buffer)
		except:
			self.register = 0
		
		self.input_buffer = ""

		return self.register
	def write_input_buffer(self, number: int):
		self.input_buffer += str(number)

		self.set_display(self.input_buffer)

	def evaluate_equation(self) -> int:
		a = self.register
		b = self.consume_input_buffer()

		result = 0

		try:
			if self.operation_mode == CalculatorOperation.Add:
				result = a + b
			elif self.operation_mode == CalculatorOperation.Subtract:
				result = a - b
			elif self.operation_mode == CalculatorOperation.Multiply:
				result = a * b
			elif self.operation_mode == CalculatorOperation.Divide:
				result = a // b # integer division because im too laxy to support floating point values
		except ZeroDivisionError:
			result = 0
			self.set_display("division by zero!")
		else:
			self.write_input_buffer(result)
			self.set_display(f"{a} {self.operation_mode} {b} = {result}")

		return result
	

	def start(self):
		self.root.mainloop()