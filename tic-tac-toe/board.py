class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[" " for _ in range(size)] for _ in range(size)]

    def display(self):
        for i, row in enumerate(self.grid):
            print(" | ".join(row))
            if i != self.size - 1:   # don't print after last row
                print("-" * (self.size * 3))

    def place_move(self, row, col, symbol):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            return False

        if self.grid[row][col] != " ":
            return False

        self.grid[row][col] = symbol.value
        return True

    def is_full(self):
        for row in self.grid:
            for cell in row:
                if cell == " ":
                    return False
        return True

    def check_winner(self, symbol):
        s = symbol.value
        n = self.size

        # rows
        for i in range(n):
            if all(self.grid[i][j] == s for j in range(n)):
                return True

        # cols
        for j in range(n):
            if all(self.grid[i][j] == s for i in range(n)):
                return True

        # diagonal
        if all(self.grid[i][i] == s for i in range(n)):
            return True

        # anti diagonal
        if all(self.grid[i][n - 1 - i] == s for i in range(n)):
            return True

        return False

