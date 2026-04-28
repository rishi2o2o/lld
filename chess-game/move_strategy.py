from abc import ABC, abstractmethod
from position import Position
from color import Color

class MoveStrategy(ABC):
    @abstractmethod
    def can_move(self, board, piece, start_pos, end_pos):
        pass


class StraightMoveStrategy(MoveStrategy):  # also rook move strategy
    def can_move(self, board, piece, start_pos, end_pos):
        
        if start_pos.row != end_pos.row and start_pos.col != end_pos.col:
            # if both row and column changed -> not a straight line -> can't move
            return False
            
        return board.is_path_clear(start_pos, end_pos)


class DiagonalMoveStrategy(MoveStrategy):  # also bishop move strategy
    def can_move(self, board, piece, start_pos, end_pos):

        if abs(start_pos.row - end_pos.row) != abs(start_pos.col - end_pos.col):
            # if start_pos and end_pos don't lie on a diagonal -> can't move
            return False

        return board.is_path_clear(start_pos, end_pos)


class QueenMoveStrategy(MoveStrategy):
    def can_move(self, board, piece, start_pos, end_pos):
        can_move_straight = StraightMoveStrategy().can_move(board, piece, start_pos, end_pos)
        can_move_diagonal = DiagonalMoveStrategy().can_move(board, piece, start_pos, end_pos)
        
        return can_move_straight or can_move_diagonal


class KnightMoveStrategy(MoveStrategy):
    def can_move(self, board, piece, start_pos, end_pos):
        dr = abs(start_pos.row - end_pos.row)  # row displacement
        dc = abs(start_pos.col - end_pos.col)  # col displacement

        return (dr, dc) in [(1, 2), (2, 1)]  # should make L shpae


class KingMoveStrategy(MoveStrategy):
    def can_move(self, board, piece, start_pos, end_pos):
        dr = abs(start_pos.row - end_pos.row)  # row displacement
        dc = abs(start_pos.col - end_pos.col)  # col displacement

        return max(dr, dc) == 1  # can move 1 place in all 8 directions


class PawnMoveStrategy(MoveStrategy):
    def can_move(self, board, piece, start_pos, end_pos):
        
        # black starts at top and white starts at bottom
        # black pawns move down (+1) and white pawns move up (-1)
        direction = -1 if piece.color == Color.WHITE else 1

        # start row of pawns
        start_row = 6 if piece.color == Color.WHITE else 1  

        dr = end_pos.row - start_pos.row  # row displacement
        dc = end_pos.col - start_pos.col  # col displacement
        
        # piece placed at end pos -> could be none or non-none
        end_piece = board.get_piece(end_pos)

        # one step forward -> is allowed if not capturing
        if dc == 0 and dr == direction and end_piece is None:
            return True

        # two steps forward -> allowed if at start_row, not capturing anything and nothing in path
        middle_piece = board.get_piece(Position(start_pos.row + direction, start_pos.col))
        if (
            dc == 0
            and start_pos.row == start_row
            and dr == 2 * direction
            and end_piece is None
            and middle_piece is None
        ):
            return True

        # diagonal capture -> allowed if capturing something
        if abs(dc) == 1 and dr == direction and end_piece is not None:
            return end_piece.color != piece.color

        return False


