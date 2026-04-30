class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def is_inside(self, pos):
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

