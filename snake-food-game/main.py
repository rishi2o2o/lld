from game import SnakeGame

game = SnakeGame(5, 5)
moves = ["R", "D", "D", "L", "U"]

for m in moves:
    print("Move:", m, "Score:", game.move(m))

