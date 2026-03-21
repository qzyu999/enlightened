from typing import Dict, Type, Optional, Tuple
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.models.piece import Piece
from chess.pieces.pawn import Pawn
from chess.pieces.rook import Rook
from chess.pieces.knight import Knight
from chess.pieces.bishop import Bishop
from chess.pieces.queen import Queen
from chess.pieces.king import King
from chess.engine.game import Game

class ChessCLI:
    """CLI class for chess game interaction."""

    PIECE_SYMBOLS: Dict[Color, Dict[Type[Piece], str]] = {
        Color.WHITE: {
            Pawn: "♙",
            Rook: "♖",
            Knight: "♘",
            Bishop: "♗",
            Queen: "♕",
            King: "♔"
        },
        Color.BLACK: {
            Pawn: "♟",
            Rook: "♜",
            Knight: "♞",
            Bishop: "♝",
            Queen: "♛",
            King: "♚"
        }
    }

    @staticmethod
    def display_board(board: Board):
        """Prints a nicely formatted board to the console."""
        print("\n    a b c d e f g h")
        print("  +-----------------+")
        for row in reversed(range(8)):
            line = f"{row + 1} | "
            for col in range(8):
                piece = board.get_piece_at(Position(row, col))
                if piece:
                    symbol = ChessCLI.PIECE_SYMBOLS[piece.color].get(type(piece), "?")
                    line += f"{symbol} "
                else:
                    # Alternating dark/light square representation for better visibility
                    if (row + col) % 2 == 0:
                        line += "· "
                    else:
                        line += "  "
            line += f"| {row + 1}"
            print(line)
        print("  +-----------------+")
        print("    a b c d e f g h\n")

    @staticmethod
    def parse_move(move_str: str) -> Optional[Tuple[Position, Position]]:
        """Parses a move string like 'e2e4' into start and end Positions."""
        move_str = move_str.strip().lower()
        if len(move_str) != 4:
            return None
        
        try:
            start_col = ord(move_str[0]) - ord('a')
            start_row = int(move_str[1]) - 1
            end_col = ord(move_str[2]) - ord('a')
            end_row = int(move_str[3]) - 1
            
            if not (0 <= start_row <= 7 and 0 <= start_col <= 7 and 
                    0 <= end_row <= 7 and 0 <= end_col <= 7):
                return None

            return (Position(start_row, start_col), Position(end_row, end_col))
        except (ValueError, IndexError):
            return None

    @staticmethod
    def position_to_algebraic(pos: Position) -> str:
        """Converts a Position to algebraic notation (e.g., Position(0,0) -> 'a1')."""
        col_char = chr(ord('a') + pos.col)
        row_char = str(pos.row + 1)
        return f"{col_char}{row_char}"

    def run(self):
        """Main game loop."""
        game = Game()
        print("Welcome to Python Chess!")
        print("Enter moves in algebraic notation (e.g., 'e2e4').")
        print("Type 'quit' to exit.")

        while True:
            self.display_board(game.board)
            status = game.get_game_status()
            print(f"Status: {status}")

            if "CHECKMATE" in status or "STALEMATE" in status:
                break

            try:
                user_input = input(f"{game.turn.name} to move: ").strip().lower()
                if user_input == 'quit':
                    break

                positions = self.parse_move(user_input)
                if not positions:
                    print("Invalid input format. Please use format like 'e2e4'.")
                    continue

                start_pos, end_pos = positions
                if game.make_move(start_pos, end_pos):
                    print(f"Moved from {user_input[:2]} to {user_input[2:]}")
                else:
                    print("Illegal move. Please try again.")

            except KeyboardInterrupt:
                print("\nGame terminated.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
