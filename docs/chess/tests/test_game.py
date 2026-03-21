import unittest
from chess.engine.game import Game
from chess.models.position import Position
from chess.models.color import Color
from chess.pieces import Pawn, King, Queen, Rook, Bishop, Knight

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_setup(self):
        self.assertEqual(self.game.turn, Color.WHITE)
        self.assertIsInstance(self.game.board.get_piece_at(Position(0, 4)), King)
        self.assertIsInstance(self.game.board.get_piece_at(Position(1, 4)), Pawn)

    def test_basic_move(self):
        start = Position(1, 4)
        end = Position(3, 4)
        self.assertTrue(self.game.make_move(start, end))
        self.assertEqual(self.game.turn, Color.BLACK)
        self.assertIsNone(self.game.board.get_piece_at(start))
        self.assertIsInstance(self.game.board.get_piece_at(end), Pawn)

    def test_invalid_move_wrong_turn(self):
        start = Position(6, 4)
        end = Position(4, 4)
        self.assertFalse(self.game.make_move(start, end))
        self.assertEqual(self.game.turn, Color.WHITE)

    def test_check_detection(self):
        self.game.board.clear()
        self.game.board.set_piece_at(Position(0, 0), King(Color.WHITE, Position(0, 0)))
        self.game.board.set_piece_at(Position(7, 7), King(Color.BLACK, Position(7, 7)))
        self.game.board.set_piece_at(Position(0, 7), Rook(Color.BLACK, Position(0, 7)))
        self.assertTrue(self.game.is_in_check(Color.WHITE))

    def test_checkmate_detection(self):
        self.game.make_move(Position(1, 5), Position(2, 5))
        self.game.make_move(Position(6, 4), Position(4, 4))
        self.game.make_move(Position(1, 6), Position(3, 6))
        self.game.make_move(Position(7, 3), Position(3, 7))
        self.assertTrue(self.game.is_checkmate(Color.WHITE))

    def test_stalemate_detection(self):
        self.game.board.clear()
        self.game.board.set_piece_at(Position(0, 0), King(Color.WHITE, Position(0, 0)))
        self.game.board.set_piece_at(Position(1, 2), Queen(Color.BLACK, Position(1, 2)))
        self.game.board.set_piece_at(Position(7, 7), King(Color.BLACK, Position(7, 7)))
        self.game.turn = Color.WHITE
        self.assertTrue(self.game.is_stalemate(Color.WHITE))

    def test_pawn_promotion_to_queen(self):
        self.game.board.clear()
        self.game.board.set_piece_at(Position(6, 0), Pawn(Color.WHITE, Position(6, 0)))
        self.game.board.set_piece_at(Position(7, 7), King(Color.BLACK, Position(7, 7)))
        self.game.board.set_piece_at(Position(0, 7), King(Color.WHITE, Position(0, 7)))
        self.game.make_move(Position(6, 0), Position(7, 0))
        self.assertIsInstance(self.game.board.get_piece_at(Position(7, 0)), Queen)

    def test_kingside_castling(self):
        # Clear paths for kingside castling
        self.game.board.set_piece_at(Position(0, 5), None) # Bishop
        self.game.board.set_piece_at(Position(0, 6), None) # Knight
        king = self.game.board.get_piece_at(Position(0, 4))
        rook = self.game.board.get_piece_at(Position(0, 7))
        
        # King and Rook haven't moved yet
        self.assertIsInstance(king, King)
        self.assertIsInstance(rook, Rook)
        
        # Execute kingside castle: e1g1
        self.assertTrue(self.game.make_move(Position(0, 4), Position(0, 6)))
        self.assertIsInstance(self.game.board.get_piece_at(Position(0, 6)), King)
        self.assertIsInstance(self.game.board.get_piece_at(Position(0, 5)), Rook)

    def test_en_passant(self):
        # Setup en passant scenario
        # 1. e2e4
        self.game.make_move(Position(1, 4), Position(3, 4))
        # 1. ... a7a6 (waste a turn for black)
        self.game.make_move(Position(6, 0), Position(5, 0))
        # 2. e4e5
        self.game.make_move(Position(3, 4), Position(4, 4))
        # 2. ... d7d5 (double move next to white pawn)
        self.game.make_move(Position(6, 3), Position(4, 3))
        
        # 3. e5xd6 (en passant capture)
        self.assertTrue(self.game.make_move(Position(4, 4), Position(5, 3)))
        # Target pawn at d5 should be gone
        self.assertIsNone(self.game.board.get_piece_at(Position(4, 3)))
        # White pawn should be at d6
        self.assertIsInstance(self.game.board.get_piece_at(Position(5, 3)), Pawn)

if __name__ == '__main__':
    unittest.main()
