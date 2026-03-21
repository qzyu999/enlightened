from typing import List, Optional, Tuple
from chess.models.board import Board
from chess.models.color import Color
from chess.models.position import Position
from chess.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess.models.piece import Piece

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = Color.WHITE
        self.move_history: List[Tuple[Position, Position, Optional[Piece]]] = []
        self.reset_board()

    def reset_board(self):
        """Initializes the board to the standard starting position."""
        self.board = Board()
        self.turn = Color.WHITE
        self.move_history = []

        # Setup Pawns
        for col in range(8):
            self.board.set_piece_at(Position(1, col), Pawn(Color.WHITE, Position(1, col)))
            self.board.set_piece_at(Position(6, col), Pawn(Color.BLACK, Position(6, col)))

        # Setup non-pawn pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(piece_order):
            self.board.set_piece_at(Position(0, col), piece_class(Color.WHITE, Position(0, col)))
            self.board.set_piece_at(Position(7, col), piece_class(Color.BLACK, Position(7, col)))

    def is_in_check(self, color: Color, board: Optional[Board] = None) -> bool:
        """Determines if the king of the given color is currently in check."""
        if board is None:
            board = self.board
        
        # 1. Find the king
        king_pos = None
        for piece in board.get_all_pieces(color):
            if isinstance(piece, King):
                king_pos = piece.position
                break
        
        if not king_pos:
            return False

        # 2. Check if any opponent piece can move to the king's position
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        for piece in board.get_all_pieces(opponent_color):
            if king_pos in piece.get_valid_moves(board):
                return True
        return False

    def get_legal_moves(self, piece: Piece) -> List[Position]:
        """Returns all moves for a piece that do not leave the king in check."""
        valid_moves = piece.get_valid_moves(self.board)
        
        # Add special moves: Castling and En Passant
        if isinstance(piece, King):
            valid_moves.extend(self._get_castling_moves(piece))
        elif isinstance(piece, Pawn):
            valid_moves.extend(self._get_en_passant_moves(piece))

        legal_moves = []
        start_pos = piece.position
        for end_pos in valid_moves:
            # Simulate move
            captured_piece = self.board.get_piece_at(end_pos)
            
            # Special case for en-passant capture
            is_en_passant = isinstance(piece, Pawn) and end_pos.col != start_pos.col and captured_piece is None
            en_passant_captured = None
            if is_en_passant:
                en_passant_pos = Position(start_pos.row, end_pos.col)
                en_passant_captured = self.board.get_piece_at(en_passant_pos)
                self.board.set_piece_at(en_passant_pos, None)

            self.board.set_piece_at(end_pos, piece)
            self.board.set_piece_at(start_pos, None)
            
            if not self.is_in_check(piece.color):
                legal_moves.append(end_pos)
            
            # Undo move
            self.board.set_piece_at(start_pos, piece)
            self.board.set_piece_at(end_pos, captured_piece)
            if is_en_passant:
                self.board.set_piece_at(Position(start_pos.row, end_pos.col), en_passant_captured)
            
        return legal_moves

    def _get_castling_moves(self, king: King) -> List[Position]:
        moves = []
        if king.has_moved or self.is_in_check(king.color):
            return moves
        
        row = 0 if king.color == Color.WHITE else 7
        
        # Kingside castling
        rook_ks = self.board.get_piece_at(Position(row, 7))
        if isinstance(rook_ks, Rook) and not rook_ks.has_moved:
            if all(self.board.is_empty(Position(row, col)) for col in [5, 6]):
                # Squares King passes through must not be under attack
                if not any(self._is_square_attacked(Position(row, col), king.color) for col in [5, 6]):
                    moves.append(Position(row, 6))
        
        # Queenside castling
        rook_qs = self.board.get_piece_at(Position(row, 0))
        if isinstance(rook_qs, Rook) and not rook_qs.has_moved:
            if all(self.board.is_empty(Position(row, col)) for col in [1, 2, 3]):
                # Squares King passes through must not be under attack
                if not any(self._is_square_attacked(Position(row, col), king.color) for col in [2, 3]):
                    moves.append(Position(row, 2))
                    
        return moves

    def _get_en_passant_moves(self, pawn: Pawn) -> List[Position]:
        moves = []
        if not self.move_history:
            return moves
            
        last_start, last_end, last_captured = self.move_history[-1]
        last_piece = self.board.get_piece_at(last_end)
        
        if isinstance(last_piece, Pawn) and abs(last_start.row - last_end.row) == 2:
            # Check if pawn is adjacent
            if pawn.position.row == last_end.row and abs(pawn.position.col - last_end.col) == 1:
                direction = 1 if pawn.color == Color.WHITE else -1
                moves.append(Position(last_end.row + direction, last_end.col))
        
        return moves

    def _is_square_attacked(self, pos: Position, color: Color) -> bool:
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        for piece in self.board.get_all_pieces(opponent_color):
            if pos in piece.get_valid_moves(self.board):
                return True
        return False

    def is_checkmate(self, color: Color) -> bool:
        if not self.is_in_check(color):
            return False
        
        for piece in self.board.get_all_pieces(color):
            if self.get_legal_moves(piece):
                return False
        return True

    def is_stalemate(self, color: Color) -> bool:
        if self.is_in_check(color):
            return False
        
        for piece in self.board.get_all_pieces(color):
            if self.get_legal_moves(piece):
                return False
        return True

    def make_move(self, start_pos: Position, end_pos: Position) -> bool:
        piece = self.board.get_piece_at(start_pos)
        if piece is None or piece.color != self.turn:
            return False
        
        legal_moves = self.get_legal_moves(piece)
        if end_pos not in legal_moves:
            return False

        # Execute special move: Castling
        if isinstance(piece, King) and abs(start_pos.col - end_pos.col) == 2:
            row = start_pos.row
            if end_pos.col == 6: # Kingside
                rook = self.board.get_piece_at(Position(row, 7))
                self.board.set_piece_at(Position(row, 5), rook)
                self.board.set_piece_at(Position(row, 7), None)
                rook.has_moved = True
            elif end_pos.col == 2: # Queenside
                rook = self.board.get_piece_at(Position(row, 0))
                self.board.set_piece_at(Position(row, 3), rook)
                self.board.set_piece_at(Position(row, 0), None)
                rook.has_moved = True

        # Execute special move: En Passant
        if isinstance(piece, Pawn) and end_pos.col != start_pos.col and self.board.is_empty(end_pos):
            self.board.set_piece_at(Position(start_pos.row, end_pos.col), None)

        # Standard move execution
        captured_piece = self.board.get_piece_at(end_pos)
        self.board.set_piece_at(end_pos, piece)
        self.board.set_piece_at(start_pos, None)
        piece.has_moved = True

        # Pawn Promotion (Basic: Auto-promote to Queen)
        if isinstance(piece, Pawn):
            if (piece.color == Color.WHITE and end_pos.row == 7) or (piece.color == Color.BLACK and end_pos.row == 0):
                self.board.set_piece_at(end_pos, Queen(piece.color, end_pos))

        self.move_history.append((start_pos, end_pos, captured_piece))
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        return True

    def get_game_status(self) -> str:
        if self.is_checkmate(self.turn):
            winner = "BLACK" if self.turn == Color.WHITE else "WHITE"
            return f"CHECKMATE! {winner} wins!"
        if self.is_stalemate(self.turn):
            return "STALEMATE! It's a draw!"
        status = f"{self.turn.name}'s turn"
        if self.is_in_check(self.turn):
            status += " (CHECK)"
        return status
