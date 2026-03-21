from typing import List, TYPE_CHECKING
from chess.models.piece import Piece
from chess.models.position import Position
from chess.models.color import Color

if TYPE_CHECKING:
    from chess.models.board import Board

class Knight(Piece):
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        moves = []
        possible_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dr, dc in possible_moves:
            try:
                new_pos = Position(self.position.row + dr, self.position.col + dc)
                target_piece = board.get_piece_at(new_pos)
                if target_piece is None or target_piece.color != self.color:
                    moves.append(new_pos)
            except ValueError:
                continue
        
        return moves
