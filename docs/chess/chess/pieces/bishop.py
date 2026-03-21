from typing import List, TYPE_CHECKING
from chess.models.piece import Piece
from chess.models.position import Position

if TYPE_CHECKING:
    from chess.models.board import Board

class Bishop(Piece):
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            curr_row, curr_col = self.position.row + dr, self.position.col + dc
            while True:
                try:
                    pos = Position(curr_row, curr_col)
                    target = board.get_piece_at(pos)
                    if target is None:
                        moves.append(pos)
                    else:
                        if target.color != self.color:
                            moves.append(pos)
                        break
                    curr_row += dr
                    curr_col += dc
                except ValueError:
                    break
        return moves
