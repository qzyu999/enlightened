import unittest
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.knight import Knight

class TestKnight(unittest.TestCase):
    def test_knight_moves_middle(self):
        board = Board()
        knight = Knight(Color.WHITE, Position(4, 4))
        board.set_piece_at(Position(4, 4), knight)
        
        moves = knight.get_valid_moves(board)
        expected = [
            Position(6, 5), Position(6, 3), Position(2, 5), Position(2, 3),
            Position(5, 6), Position(5, 2), Position(3, 6), Position(3, 2)
        ]
        self.assertEqual(len(moves), 8)
        for move in expected:
            self.assertIn(move, moves)

    def test_knight_moves_edge(self):
        board = Board()
        knight = Knight(Color.WHITE, Position(0, 0))
        board.set_piece_at(Position(0, 0), knight)
        
        moves = knight.get_valid_moves(board)
        expected = [Position(2, 1), Position(1, 2)]
        self.assertEqual(len(moves), 2)
        for move in expected:
            self.assertIn(move, moves)

    def test_knight_blocked_by_own(self):
        board = Board()
        knight = Knight(Color.WHITE, Position(4, 4))
        own_piece = Knight(Color.WHITE, Position(6, 5))
        board.set_piece_at(Position(4, 4), knight)
        board.set_piece_at(Position(6, 5), own_piece)
        
        moves = knight.get_valid_moves(board)
        self.assertEqual(len(moves), 7)
        self.assertNotIn(Position(6, 5), moves)

if __name__ == '__main__':
    unittest.main()
