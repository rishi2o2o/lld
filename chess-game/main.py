from color import Color
from position import Position
from game_status import GameStatus
from game import Game

def parse_position(text):
    text = text.strip().lower()

    if len(text) != 2:
        raise ValueError("Use chess notation like e2 or g8")

    file_char = text[0]
    rank_char = text[1]

    if file_char < "a" or file_char > "h" or rank_char < "1" or rank_char > "8":
        raise ValueError("Position must be between a1 and h8")

    col = ord(file_char) - ord("a")
    row = 8 - int(rank_char)
    return Position(row, col)


def parse_move(text):
    parts = text.strip().split()

    if len(parts) != 2:
        raise ValueError("Enter move as: e2 e4")

    return parse_position(parts[0]), parse_position(parts[1])


def main():
    game = Game()

    print("Command-line Chess")
    print("White pieces are uppercase. Black pieces are lowercase.")
    print("Enter moves like: e2 e4")
    print("Type 'quit' to exit.")

    while game.game_status not in (GameStatus.CHECKMATE, GameStatus.STALEMATE):
        game.board.print_board()
        print(f"Status: {game.game_status.name}")
        move_text = input(f"{game.cur_color.name.capitalize()} to move > ").strip()

        if move_text.lower() in ("quit", "exit"):
            print("Game ended.")
            return

        try:
            start, end = parse_move(move_text)
            game.make_move(start, end)
        except ValueError as error:
            print(f"Invalid move: {error}")

    game.board.print_board()
    print(f"Game over: {game.game_status.name}")

    if game.game_status == GameStatus.CHECKMATE:
        winner = Color.BLACK if game.cur_color == Color.WHITE else Color.WHITE
        print(f"{winner.name.capitalize()} wins!")
    else:
        print("Draw by stalemate.")


if __name__ == "__main__":
    main()
