from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from chess.models.color import Color
from chess.models.position import Position

if TYPE_CHECKING:
    from chess.models.board import Board

class Piece(ABC):
    def __init__(self, color: Color, position: Position):
        self.color = color
        self.position = position
        self.has_moved = False

    @abstractmethod
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        """Returns a list of valid moves for this piece."""
        pass

    def __repr__(self):
        return f"{self.color.name} {self.__class__.__name__} at {self.position}"
