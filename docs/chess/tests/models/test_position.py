import unittest
from chess.models.position import Position

class TestPosition(unittest.TestCase):
    def test_position_creation(self):
        pos = Position(3, 4)
        self.assertEqual(pos.row, 3)
        self.assertEqual(pos.col, 4)

    def test_position_is_valid(self):
        self.assertTrue(Position.is_valid(0, 0))
        self.assertTrue(Position.is_valid(7, 7))
        self.assertFalse(Position.is_valid(-1, 0))
        self.assertFalse(Position.is_valid(8, 0))

    def test_position_out_of_bounds(self):
        with self.assertRaises(ValueError):
            Position(-1, 0)
        with self.assertRaises(ValueError):
            Position(0, 8)

if __name__ == '__main__':
    unittest.main()
