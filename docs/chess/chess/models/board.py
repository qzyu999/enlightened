from typing import Optional, List, Dict
from chess.models.position import Position
from chess.models.piece import Piece
from chess.models.color import Color

class Board:
    def __init__(self):
        self._grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]

    def get_piece_at(self, position: Position) -> Optional[Piece]:
        return self._grid[position.row][position.col]

    def set_piece_at(self, position: Position, piece: Optional[Piece]):
        if piece is not None:
            piece.position = position
        self._grid[position.row][position.col] = piece

    def is_empty(self, position: Position) -> bool:
        return self._grid[position.row][position.col] is None

    def clear(self):
        """Clears the board of all pieces."""
        self._grid = [[None for _ in range(8)] for _ in range(8)]

    def get_all_pieces(self, color: Optional[Color] = None) -> List[Piece]:
        pieces = []
        for row in self._grid:
            for item in row:
                if item is not None:
                    if color is None or item.color == color:
                        pieces.append(item)
        return pieces

    def __repr__(self):
        result = ""
        for row in reversed(range(8)):
            result += f"{row} "
            for col in range(8):
                piece = self._grid[row][col]
                if piece:
                    # Temporary visualization: shorthand for piece name (e.g., 'WP' for white pawn)
                    color_char = 'W' if piece.color == Color.WHITE else 'B'
                    piece_char = piece.__class__.__name__[0]
                    result += f"[{color_char}{piece_char}]"
                else:
                    result += "[  ]"
            result += "\n"
        result += "   0   1   2   3   4   5   6   7"
        return result
