import unittest
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.bishop import Bishop

class TestBishop(unittest.TestCase):
    def test_bishop_moves_middle(self):
        board = Board()
        bishop = Bishop(Color.WHITE, Position(4, 4))
        board.set_piece_at(Position(4, 4), bishop)
        
        moves = bishop.get_valid_moves(board)
        # 4 directions:
        # (5,5), (6,6), (7,7)
        # (5,3), (6,2), (7,1)
        # (3,5), (2,6), (1,7)
        # (3,3), (2,2), (1,1), (0,0)
        self.assertEqual(len(moves), 13)
        self.assertIn(Position(0, 0), moves)
        self.assertIn(Position(7, 7), moves)
        self.assertIn(Position(7, 1), moves)
        self.assertIn(Position(1, 7), moves)

    def test_bishop_blocked_by_own(self):
        board = Board()
        bishop = Bishop(Color.WHITE, Position(4, 4))
        own_piece = Bishop(Color.WHITE, Position(6, 6))
        board.set_piece_at(Position(4, 4), bishop)
        board.set_piece_at(Position(6, 6), own_piece)
        
        moves = bishop.get_valid_moves(board)
        self.assertIn(Position(5, 5), moves)
        self.assertNotIn(Position(6, 6), moves)
        self.assertNotIn(Position(7, 7), moves)
        self.assertEqual(len(moves), 11)

    def test_bishop_capture(self):
        board = Board()
        bishop = Bishop(Color.WHITE, Position(4, 4))
        target = Bishop(Color.BLACK, Position(6, 6))
        board.set_piece_at(Position(4, 4), bishop)
        board.set_piece_at(Position(6, 6), target)
        
        moves = bishop.get_valid_moves(board)
        self.assertIn(Position(5, 5), moves)
        self.assertIn(Position(6, 6), moves)
        self.assertNotIn(Position(7, 7), moves)
        self.assertEqual(len(moves), 12)

if __name__ == '__main__':
    unittest.main()
