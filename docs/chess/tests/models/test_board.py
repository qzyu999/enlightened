import unittest
from chess.models.board import Board
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces.pawn import Pawn

class TestBoard(unittest.TestCase):
    def test_board_initialization(self):
        board = Board()
        for r in range(8):
            for c in range(8):
                self.assertTrue(board.is_empty(Position(r, c)))

    def test_set_get_piece(self):
        board = Board()
        pos = Position(1, 1)
        pawn = Pawn(Color.WHITE, pos)
        board.set_piece_at(pos, pawn)
        
        self.assertEqual(board.get_piece_at(pos), pawn)
        self.assertFalse(board.is_empty(pos))

    def test_get_all_pieces(self):
        board = Board()
        p1 = Pawn(Color.WHITE, Position(1, 1))
        p2 = Pawn(Color.BLACK, Position(6, 1))
        board.set_piece_at(Position(1, 1), p1)
        board.set_piece_at(Position(6, 1), p2)
        
        all_pieces = board.get_all_pieces()
        self.assertEqual(len(all_pieces), 2)
        self.assertIn(p1, all_pieces)
        self.assertIn(p2, all_pieces)
        
        white_pieces = board.get_all_pieces(Color.WHITE)
        self.assertEqual(len(white_pieces), 1)
        self.assertIn(p1, white_pieces)
        self.assertNotIn(p2, white_pieces)

if __name__ == '__main__':
    unittest.main()
