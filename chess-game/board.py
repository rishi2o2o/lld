from position import Position
from color import Color
from piece_factory import PieceFactory

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # assume 8x8 board

    def is_inside(self, pos):
        return 0 <= pos.row < 8 and 0 <= pos.col < 8

    def get_piece(self, pos):
        return self.grid[pos.row][pos.col]

    def set_piece(self, pos, piece):
        self.grid[pos.row][pos.col] = piece

    def move_piece(self, start, end):
        start_piece = self.get_piece(start)  # get piece at start pos
        end_piece = self.get_piece(end)  # get piece at end pos
        self.set_piece(end, start_piece)  # move start piece to end
        self.set_piece(start, None)  # empty start pos
        return end_piece  # return captured piece

    def undo_move(self, start, end, captured):
        piece = self.get_piece(end)
        self.set_piece(start, piece)
        self.set_piece(end, captured)

    def is_path_clear(self, start_pos, end_pos):
        row_step = self._sign(end_pos.row - start_pos.row)
        col_step = self._sign(end_pos.col - start_pos.col)

        row = start_pos.row + row_step
        col = start_pos.col + col_step

        while row != end_pos.row or col != end_pos.col:
            if self.grid[row][col] is not None:  # some piece is in path
                return False
            row += row_step
            col += col_step

        return True  # path empty

    def setup(self):
        order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]  
        # order is same for both colors, both kings face each other at start

        for col, piece_type in enumerate(order):
            self.set_piece(Position(0, col), PieceFactory.create(piece_type, Color.BLACK))  # place black at top
            self.set_piece(Position(7, col), PieceFactory.create(piece_type, Color.WHITE))  # place white at bottom

        for col in range(8):
            self.set_piece(Position(1, col), PieceFactory.create("pawn", Color.BLACK))
            self.set_piece(Position(6, col), PieceFactory.create("pawn", Color.WHITE))

    def _sign(self, value):
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def print_board(self):
        print()
        for row in range(8):
            rank = 8 - row
            cells = []
            for col in range(8):
                piece = self.grid[row][col]
                cells.append(piece.display() if piece else ".")
            print(f"{rank}  {' '.join(cells)}")
        print()
        print("   a b c d e f g h")
        print()


