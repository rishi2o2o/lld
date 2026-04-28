from enum import Enum, auto

class GameStatus(Enum):
    ACTIVE = auto()
    CHECK = auto()
    CHECKMATE = auto()
    STALEMATE = auto()

