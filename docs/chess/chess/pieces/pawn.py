from typing import List, TYPE_CHECKING
from chess.models.piece import Piece
from chess.models.position import Position
from chess.models.color import Color

if TYPE_CHECKING:
    from chess.models.board import Board

class Pawn(Piece):
    def get_valid_moves(self, board: 'Board') -> List[Position]:
        moves = []
        direction = 1 if self.color == Color.WHITE else -1
        
        # Forward move
        try:
            forward_pos = Position(self.position.row + direction, self.position.col)
            if board.is_empty(forward_pos):
                moves.append(forward_pos)
                # Double forward move from starting position
                start_row = 1 if self.color == Color.WHITE else 6
                if self.position.row == start_row:
                    double_forward = Position(self.position.row + 2 * direction, self.position.col)
                    if board.is_empty(double_forward):
                        moves.append(double_forward)
        except ValueError:
            pass

        # Captures
        for dc in [-1, 1]:
            try:
                capture_pos = Position(self.position.row + direction, self.position.col + dc)
                target_piece = board.get_piece_at(capture_pos)
                if target_piece and target_piece.color != self.color:
                    moves.append(capture_pos)
            except ValueError:
                continue

        return moves
