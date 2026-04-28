from position import Position
from board import Board
from color import Color
from game_status import GameStatus
from piece import King, Queen, Pawn

class Game:
    def __init__(self):
        self.board = Board()
        self.board.setup()
        self.cur_color = Color.WHITE  # white starts first
        self.game_status = GameStatus.ACTIVE

    def make_move(self, start_pos, end_pos):
        start_piece = self.board.get_piece(start_pos)

        if start_piece is None:
            raise Exception("No piece at source")

        if start_piece.color != self.cur_color:
            raise Exception("Not this player's turn")

        if not start_piece.can_move(self.board, start_pos, end_pos):
            raise Exception("Invalid move for piece")

        captured_piece = self.board.move_piece(start_pos, end_pos)

        if self.is_in_check(self.cur_color):
            self.board.undo_move(start_pos, end_pos, captured_piece)
            raise Exception("Move leaves king in check")

        self._promote_pawn_if_needed(end_pos)

        opp_color = Color.BLACK if self.cur_color == Color.WHITE else Color.WHITE 

        if self.is_in_check(opp_color):
            self.game_status = GameStatus.CHECKMATE if not self.has_legal_move(opp_color) else GameStatus.CHECK
        else:
            self.game_status = GameStatus.STALEMATE if not self.has_legal_move(opp_color) else GameStatus.ACTIVE

        self.cur_color = opp_color


    def is_in_check(self, color):
        king_pos = self._find_king(color)

        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = self.board.get_piece(pos)

                if piece is not None and piece.color != color:
                    if piece.can_move(self.board, pos, king_pos):  # if any opp color piece can reach cur king
                        return True

        return False


    def has_legal_move(self, color):
        for sr in range(8):
            for sc in range(8):
                start_pos = Position(sr, sc)
                start_piece = self.board.get_piece(start_pos)

                if start_piece is None or start_piece.color != color:
                    continue

                for er in range(8):
                    for ec in range(8):
                        end_pos = Position(er, ec)

                        if start_piece.can_move(self.board, start_pos, end_pos):
                            # if start piece can move to end pos without check
                            captured_piece = self.board.move_piece(start_pos, end_pos)
                            in_check = self.is_in_check(color)

                            self.board.undo_move(start_pos, end_pos, captured_piece)  # revert move

                            if not in_check:
                                return True

        return False


    def _find_king(self, color):
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = self.board.get_piece(pos)
                if isinstance(piece, King) and piece.color == color:
                    return pos

        raise Exception("King not found")


    def _promote_pawn_if_needed(self, pos):
        piece = self.board.get_piece(pos)

        if isinstance(piece, Pawn):
            if piece.color == Color.WHITE and pos.row == 0:  # white pawn reached top
                self.board.set_piece(pos, Queen(Color.WHITE))

            elif piece.color == Color.BLACK and pos.row == 7:  # black pawn reached bottom
                self.board.set_piece(pos, Queen(Color.BLACK))



