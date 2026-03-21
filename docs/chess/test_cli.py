from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.pawn import Pawn
from chess.pieces.rook import Rook
from chess.pieces.knight import Knight
from chess.pieces.bishop import Bishop
from chess.pieces.queen import Queen
from chess.pieces.king import King
from chess.ui.cli import ChessCLI

def test_display():
    board = Board()
    
    # Set up some pieces
    # White pawns on row 1 (a2, b2, ..., h2)
    for col in range(8):
        board.set_piece_at(Position(1, col), Pawn(Color.WHITE, Position(1, col)))
    
    # White back rank
    board.set_piece_at(Position(0, 0), Rook(Color.WHITE, Position(0, 0)))
    board.set_piece_at(Position(0, 1), Knight(Color.WHITE, Position(0, 1)))
    board.set_piece_at(Position(0, 2), Bishop(Color.WHITE, Position(0, 2)))
    board.set_piece_at(Position(0, 3), Queen(Color.WHITE, Position(0, 3)))
    board.set_piece_at(Position(0, 4), King(Color.WHITE, Position(0, 4)))
    board.set_piece_at(Position(0, 5), Bishop(Color.WHITE, Position(0, 5)))
    board.set_piece_at(Position(0, 6), Knight(Color.WHITE, Position(0, 6)))
    board.set_piece_at(Position(0, 7), Rook(Color.WHITE, Position(0, 7)))

    # Black pawns on row 6 (a7, b7, ..., h7)
    for col in range(8):
        board.set_piece_at(Position(6, col), Pawn(Color.BLACK, Position(6, col)))
        
    # Black back rank
    board.set_piece_at(Position(7, 0), Rook(Color.BLACK, Position(7, 0)))
    board.set_piece_at(Position(7, 1), Knight(Color.BLACK, Position(7, 1)))
    board.set_piece_at(Position(7, 2), Bishop(Color.BLACK, Position(7, 2)))
    board.set_piece_at(Position(7, 3), Queen(Color.BLACK, Position(7, 3)))
    board.set_piece_at(Position(7, 4), King(Color.BLACK, Position(7, 4)))
    board.set_piece_at(Position(7, 5), Bishop(Color.BLACK, Position(7, 5)))
    board.set_piece_at(Position(7, 6), Knight(Color.BLACK, Position(7, 6)))
    board.set_piece_at(Position(7, 7), Rook(Color.BLACK, Position(7, 7)))

    ChessCLI.display_board(board)

def test_parsing():
    move = "e2e4"
    positions = ChessCLI.parse_move(move)
    if positions:
        start, end = positions
        print(f"Move {move}: Start={start}, End={end}")
        print(f"Algebraic: {ChessCLI.position_to_algebraic(start)} to {ChessCLI.position_to_algebraic(end)}")
    else:
        print(f"Invalid move: {move}")

if __name__ == "__main__":
    test_display()
    test_parsing()
