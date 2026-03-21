import unittest
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.queen import Queen

class TestQueen(unittest.TestCase):
    def test_queen_moves_middle(self):
        board = Board()
        queen = Queen(Color.WHITE, Position(4, 4))
        board.set_piece_at(Position(4, 4), queen)
        
        moves = queen.get_valid_moves(board)
        # Queen = Rook (14) + Bishop (13) = 27 moves
        self.assertEqual(len(moves), 27)

    def test_queen_blocked(self):
        board = Board()
        queen = Queen(Color.WHITE, Position(4, 4))
        own_piece = Queen(Color.WHITE, Position(6, 4))
        target = Queen(Color.BLACK, Position(6, 6))
        board.set_piece_at(Position(4, 4), queen)
        board.set_piece_at(Position(6, 4), own_piece)
        board.set_piece_at(Position(6, 6), target)
        
        moves = queen.get_valid_moves(board)
        # Vertically blocked: (5,4) ok, (6,4) no
        self.assertIn(Position(5, 4), moves)
        self.assertNotIn(Position(6, 4), moves)
        # Diagonally capture: (5,5) ok, (6,6) ok, (7,7) no
        self.assertIn(Position(5, 5), moves)
        self.assertIn(Position(6, 6), moves)
        self.assertNotIn(Position(7, 7), moves)

if __name__ == '__main__':
    unittest.main()
