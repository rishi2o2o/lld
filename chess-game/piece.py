from abc import ABC
from color import Color
from move_strategy import KingMoveStrategy, QueenMoveStrategy, StraightMoveStrategy, DiagonalMoveStrategy, KnightMoveStrategy, PawnMoveStrategy

class Piece(ABC):
    symbol = "?"

    def __init__(self, color, move_strategy):
        self.color = color
        self.move_strategy = move_strategy

    def can_move(self, board, start_pos, end_pos):
        if not board.is_inside(end_pos):
            return False

        end_piece = board.get_piece(end_pos)

        if end_piece is not None and end_piece.color == self.color:
            return False

        return self.move_strategy.can_move(board, self, start_pos, end_pos)

    def display(self):
        return self.symbol.upper() if self.color == Color.WHITE else self.symbol.lower()

class King(Piece):
    symbol = "K"

    def __init__(self, color):
        super().__init__(color, KingMoveStrategy())


class Queen(Piece):
    symbol = "Q"

    def __init__(self, color):
        super().__init__(color, QueenMoveStrategy())


class Rook(Piece):
    symbol = "R"

    def __init__(self, color):
        super().__init__(color, StraightMoveStrategy())


class Bishop(Piece):
    symbol = "B"

    def __init__(self, color):
        super().__init__(color, DiagonalMoveStrategy())


class Knight(Piece):
    symbol = "N"

    def __init__(self, color):
        super().__init__(color, KnightMoveStrategy())


class Pawn(Piece):
    symbol = "P"

    def __init__(self, color):
        super().__init__(color, PawnMoveStrategy())


