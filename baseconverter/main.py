BASE_SET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def intput(prompt: str) -> int:
	try:
		return int(input(prompt))
	except ValueError:
		print("\x1b[31mInvalid number!\x1b[0m")

		return intput(prompt)

def tonumber(text: str, base: int) -> int:
	output = 0

	for (position, char) in enumerate(reversed(text)):
		index = BASE_SET.index(char)

		if index >= base:
			raise ValueError(f"Character '{char}' is out of range for base {base}")

		output += index * (base ** position)

	return output

def tobase(num: int, base: int) -> str:
	output = ""

	value = num

	while value > 0:
		remainder = value % base
		value = value // base

		char = BASE_SET[remainder]

		output = char + output

	return output

while True:
	text = input("value: ")
	base_from = intput("from base: ")
	base_target = intput("target base: ")

	value = tonumber(text, base_from)
	converted = tobase(value, base_target)

	print("=" * 32)
	print(f"Base {base_from}: {text}\nBase {base_target}: {converted}")
	print("=" * 32)