import unittest
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.rook import Rook

class TestRook(unittest.TestCase):
    def test_rook_moves_middle(self):
        board = Board()
        rook = Rook(Color.WHITE, Position(4, 4))
        board.set_piece_at(Position(4, 4), rook)
        
        moves = rook.get_valid_moves(board)
        # 4 directions: 4 rows + 4 cols minus the Rook itself
        # Up (5,6,7), Down (3,2,1,0), Right (5,6,7), Left (3,2,1,0)
        self.assertEqual(len(moves), 14)
        self.assertIn(Position(4, 0), moves)
        self.assertIn(Position(4, 7), moves)
        self.assertIn(Position(0, 4), moves)
        self.assertIn(Position(7, 4), moves)

    def test_rook_blocked(self):
        board = Board()
        rook = Rook(Color.WHITE, Position(4, 4))
        own_piece = Rook(Color.WHITE, Position(6, 4))
        target = Rook(Color.BLACK, Position(4, 6))
        board.set_piece_at(Position(4, 4), rook)
        board.set_piece_at(Position(6, 4), own_piece)
        board.set_piece_at(Position(4, 6), target)
        
        moves = rook.get_valid_moves(board)
        # Vertically up: blocked at (6,4) -> (5,4)
        self.assertIn(Position(5, 4), moves)
        self.assertNotIn(Position(6, 4), moves)
        self.assertNotIn(Position(7, 4), moves)
        # Horizontally right: capture at (4,6) -> (4,5), (4,6)
        self.assertIn(Position(4, 5), moves)
        self.assertIn(Position(4, 6), moves)
        self.assertNotIn(Position(4, 7), moves)
        self.assertEqual(len(moves), 4 + 1 + 2 + 4) # Left(4), Up(1), Right(2), Down(4)

if __name__ == '__main__':
    unittest.main()
