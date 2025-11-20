from enum import Enum

class KeypadCommand:
	SetOperation = "SetOperation"
	WriteNumber = "WriteNumber"
	Clear = "Clear"
	Evaluate = "Evaluate"

class CalculatorOperation:
	Add = "+"
	Subtract = "-"
	Multiply = "*"
	Divide = "//"