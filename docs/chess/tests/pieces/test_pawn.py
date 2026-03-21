import unittest
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.pawn import Pawn

class TestPawn(unittest.TestCase):
    def test_pawn_initial_moves_white(self):
        board = Board()
        pawn = Pawn(Color.WHITE, Position(1, 1))
        board.set_piece_at(Position(1, 1), pawn)
        
        moves = pawn.get_valid_moves(board)
        self.assertIn(Position(2, 1), moves)
        self.assertIn(Position(3, 1), moves)
        self.assertEqual(len(moves), 2)

    def test_pawn_initial_moves_black(self):
        board = Board()
        pawn = Pawn(Color.BLACK, Position(6, 4))
        board.set_piece_at(Position(6, 4), pawn)
        
        moves = pawn.get_valid_moves(board)
        self.assertIn(Position(5, 4), moves)
        self.assertIn(Position(4, 4), moves)
        self.assertEqual(len(moves), 2)

    def test_pawn_blocked_forward(self):
        board = Board()
        pawn = Pawn(Color.WHITE, Position(1, 1))
        blocking_piece = Pawn(Color.BLACK, Position(2, 1))
        board.set_piece_at(Position(1, 1), pawn)
        board.set_piece_at(Position(2, 1), blocking_piece)
        
        moves = pawn.get_valid_moves(board)
        self.assertEqual(len(moves), 0)

    def test_pawn_captures(self):
        board = Board()
        pawn = Pawn(Color.WHITE, Position(1, 1))
        target1 = Pawn(Color.BLACK, Position(2, 0))
        target2 = Pawn(Color.BLACK, Position(2, 2))
        board.set_piece_at(Position(1, 1), pawn)
        board.set_piece_at(Position(2, 0), target1)
        board.set_piece_at(Position(2, 2), target2)
        
        moves = pawn.get_valid_moves(board)
        self.assertIn(Position(2, 0), moves)
        self.assertIn(Position(2, 2), moves)
        self.assertIn(Position(2, 1), moves) # Forward
        self.assertIn(Position(3, 1), moves) # Double forward
        self.assertEqual(len(moves), 4)

if __name__ == '__main__':
    unittest.main()
