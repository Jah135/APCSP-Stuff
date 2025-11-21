from enum import IntEnum
from time import sleep
from random import randint

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
    
    def turn(self, target: Facing) -> bool:
        if ((self.facing == Facing.Right and target == Facing.Left)
            or (self.facing == Facing.Down and target == Facing.Up)
            or (self.facing == Facing.Left and target == Facing.Right)
            or (self.facing == Facing.Up and target == Facing.Down)):
            return False

        self.facing = target

        return True
    def turn_right(self):
        self.turn(Facing((self.facing + 1) % 4))
    def turn_left(self):
        self.turn(Facing((self.facing - 1) % 4))

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


def render_game() -> str:
    output = ""

    for y in range(10):
        for x in range(10):
            if (x, y) in snake.body:
                output += "# "
            else:
                output += ". "
        output += "\n"
    
    return output

snake = Snake()

while True:
    snake.update()
    print(render_game())
    sleep(0.1)

    if randint(0, 10) > 5:
        snake.turn_right()
    else:
        pass    