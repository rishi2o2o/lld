import random
from board import Board
from position import Position
from food import Food
from snake import Snake

class SnakeGame:
    DIRECTIONS = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    def __init__(self, rows, cols):
        self.board = Board(rows, cols)
        self.snake = Snake(Position(0, 0))
        self.food = self._generate_food()  # assume only 1 food
        self.score = 0
        self.game_over = False

    def _generate_food(self):
        while True:
            pos = Position(
                random.randint(0, self.board.rows-1),
                random.randint(0, self.board.cols-1),
            )
            if pos not in self.snake.body_set:
                return Food(pos)

    def move(self, direction):
        if self.game_over:
            return -1

        dr, dc = self.DIRECTIONS[direction]
        head = self.snake.get_head()

        # compute new head
        new_head = Position(head.row+dr, head.col+dc)

        # check wall collision
        if not self.board.is_inside(new_head):
            self.game_over = True
            return -1
        
        # grow if you land on a food piece
        if new_head == self.food.position:
            grow = True
            self.score += 1
            self.food = self._generate_food()
        else:
            grow = False
        
        # check self collision
        if self.snake.will_collide(new_head, grow):
            self.game_over = True
            return -1

        # move snake
        self.snake.move(new_head, grow)

        # return score
        return self.score
        

