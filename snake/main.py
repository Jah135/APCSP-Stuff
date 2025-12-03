from enum import IntEnum
from random import randint
from time import sleep, perf_counter
from keyboard import is_pressed

SNAKE_BODY_CHAR = "# "
SNAKE_HEAD_CHAR = "O "
FRUIT_CHAR = "X "
EMPTY_CHAR = ". "

WIDTH = 10
HEIGHT = 10

GAME_RATE = 10

class Facing(IntEnum):
	Right = 0
	Down = 1
	Left = 2
	Up = 3

class Snake:
	def __init__(self) -> None:
		self.body = [(3, 0), (2, 0), (1, 0), (0, 0)] # 0 index is the head, as the body grows positions will be appended
		self.facing = Facing.Right
		# 0 -> Right
		# 1 -> Down
		# 2 -> Left
		# 3 -> Up
	
	def turn_to(self, target: Facing) -> bool:
		if ((self.facing == Facing.Right and target == Facing.Left)
			or (self.facing == Facing.Down and target == Facing.Up)
			or (self.facing == Facing.Left and target == Facing.Right)
			or (self.facing == Facing.Up and target == Facing.Down)):
			return False

		self.facing = target

		return True
	def turn_right(self):
		self.turn_to(Facing((self.facing + 1) % 4))
	def turn_left(self):
		self.turn_to(Facing((self.facing - 1) % 4))

	def update(self):
		for index in range(len(self.body) - 1, 0, -1):
			self.body[index] = self.body[index - 1]
		
		head_x, head_y = self.body[0]

		if self.facing == Facing.Right:
			self.body[0] = (head_x + 1, head_y)
		elif self.facing == Facing.Down:
			self.body[0] = (head_x, head_y + 1)
		elif self.facing == Facing.Left:
			self.body[0] = (head_x - 1, head_y)
		elif self.facing == Facing.Up:
			self.body[0] = (head_x, head_y - 1)

snake = Snake()
fruit_position = (5, 5)
score = 0

def render_game() -> str:
	output = ""

	head_pos = snake.body[0]

	for y in range(HEIGHT):
		for x in range(WIDTH):
			p = (x, y)

			if p == head_pos:
				output += SNAKE_HEAD_CHAR
			elif p in snake.body:
				output += SNAKE_BODY_CHAR
			elif p == fruit_position:
				output += FRUIT_CHAR
			else:
				output += EMPTY_CHAR
		output += "\n"
	
	output += f"\nScore: {score}"
	
	return output
def handle_input():
	if is_pressed("w"):
		snake.turn_to(Facing.Up)
	elif is_pressed("a"):
		snake.turn_to(Facing.Left)
	elif is_pressed("s"):
		snake.turn_to(Facing.Down)
	elif is_pressed("d"):
		snake.turn_to(Facing.Right)

def update_game():
	global score
	global fruit_position

	last_tail = snake.body[len(snake.body) - 1]

	snake.update()

	head_pos = snake.body[0]

	if head_pos[0] < 0 or head_pos[0] >= WIDTH or head_pos[1] < 0 or head_pos[1] >= HEIGHT or snake.body.count(head_pos) > 1:
		print("bro died")
		return False

	if head_pos == fruit_position:
		score += 1

		fruit_position = (randint(0, WIDTH - 1), randint(0, HEIGHT - 1))
		snake.body.append(last_tail)
	
	return True

next_move = 0

while True:
	if perf_counter() >= next_move:
		next_move = perf_counter() + (1 / GAME_RATE)
		if not update_game():
			break
		
		print(render_game())
		
	handle_input()

	sleep(0.01)