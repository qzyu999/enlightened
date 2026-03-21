from typing import List, TYPE_CHECKING
from chess.models.piece import Piece
from chess.models.position import Position

if TYPE_CHECKING:
    from chess.models.board import Board

class King(Piece):
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in directions:
            try:
                new_pos = Position(self.position.row + dr, self.position.col + dc)
                target = board.get_piece_at(new_pos)
                if target is None or target.color != self.color:
                    moves.append(new_pos)
            except ValueError:
                continue
        return moves
