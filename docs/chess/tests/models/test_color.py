import unittest
from chess.models.color import Color

class TestColor(unittest.TestCase):
    def test_color_values(self):
        self.assertIsNotNone(Color.WHITE)
        self.assertIsNotNone(Color.BLACK)
        self.assertNotEqual(Color.WHITE, Color.BLACK)

    def test_opponent(self):
        self.assertEqual(Color.WHITE.opponent(), Color.BLACK)
        self.assertEqual(Color.BLACK.opponent(), Color.WHITE)

if __name__ == '__main__':
    unittest.main()
