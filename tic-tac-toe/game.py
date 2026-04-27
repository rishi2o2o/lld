from board import Board
from symbol import Symbol
from player import Player
from game_status import GameStatus

class Game:
    def __init__(self):
        self.board = Board(3)
        self.players = [
            Player("Player1", Symbol.X),
            Player("Player2", Symbol.O)
        ]
        self.current = 0
        self.status = GameStatus.IN_PROGRESS

    def switch_turn(self):
        self.current = 1 - self.current

    def start(self):
        while self.status == GameStatus.IN_PROGRESS:
            self.board.display()

            player = self.players[self.current]
            print(f"{player.name}'s turn ({player.symbol.value})")

            row = int(input("Row: "))
            col = int(input("Col: "))

            if not self.board.place_move(row, col, player.symbol):
                print("Invalid move. Try again.")
                continue

            if self.board.check_winner(player.symbol):
                self.status = GameStatus.WIN
                self.board.display()
                print(f"{player.name} wins!")
                return

            if self.board.is_full():
                self.status = GameStatus.DRAW
                self.board.display()
                print("Draw!")
                return

            self.switch_turn()


