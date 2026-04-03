"""Unit tests for Card module."""
import unittest
import sys
sys.path.insert(0, '.')
from src.card import Card, Suit, Rank


class TestSuit(unittest.TestCase):
    """Tests for Suit enum."""
    
    def test_suit_values_exist(self):
        """Verify all suits exist."""
        self.assertEqual(Suit.HEARTS.value, "♥")
        self.assertEqual(Suit.DIAMONDS.value, "♦")
        self.assertEqual(Suit.CLUBS.value, "♣")
        self.assertEqual(Suit.SPADES.value, "♠")
    
    def test_suit_count(self):
        """Verify exactly 4 suits."""
        self.assertEqual(len(list(Suit)), 4)


class TestRank(unittest.TestCase):
    """Tests for Rank enum."""
    
    def test_rank_values(self):
        """Verify rank values."""
        self.assertEqual(Rank.TWO.value, "2")
        self.assertEqual(Rank.TEN.value, "10")
        self.assertEqual(Rank.JACK.value, "J")
        self.assertEqual(Rank.QUEEN.value, "Q")
        self.assertEqual(Rank.KING.value, "K")
        self.assertEqual(Rank.ACE.value, "A")
    
    def test_rank_count(self):
        """Verify exactly 13 ranks."""
        self.assertEqual(len(list(Rank)), 13)


class TestCard(unittest.TestCase):
    """Tests for Card class."""
    
    def test_card_creation(self):
        """Test card creation with suit and rank."""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
    
    def test_card_value_number(self):
        """Test card value for numbered cards."""
        card = Card(Suit.CLUBS, Rank.SEVEN)
        self.assertEqual(card.value, 7)
    
    def test_card_value_face(self):
        """Test card value for face cards."""
        jack = Card(Suit.SPADES, Rank.JACK)
        queen = Card(Suit.HEARTS, Rank.QUEEN)
        king = Card(Suit.DIAMONDS, Rank.KING)
        self.assertEqual(jack.value, 10)
        self.assertEqual(queen.value, 10)
        self.assertEqual(king.value, 10)
    
    def test_card_value_ace(self):
        """Test card value for Ace."""
        ace = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(ace.value, 11)
    
    def test_card_str(self):
        """Test string representation."""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(str(card), "A♥")
    
    def test_card_repr(self):
        """Test repr representation."""
        card = Card(Suit.SPADES, Rank.KING)
        self.assertEqual(repr(card), "Card(SPADES, KING)")
    
    def test_card_equality(self):
        """Test card equality."""
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.HEARTS, Rank.ACE)
        card3 = Card(Suit.SPADES, Rank.ACE)
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
