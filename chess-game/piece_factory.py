from piece import King, Queen, Rook, Bishop, Knight, Pawn

class PieceFactory:
    @staticmethod
    def create(piece_type, color):

        pieces = {
            "king": King,
            "queen": Queen,
            "rook": Rook,
            "bishop": Bishop,
            "knight": Knight,
            "pawn": Pawn,
        }
        
        return pieces[piece_type](color)

