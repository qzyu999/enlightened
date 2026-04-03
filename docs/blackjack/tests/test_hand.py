"""Unit tests for Hand module."""
import unittest
import sys
sys.path.insert(0, '.')
from src.hand import Hand
from src.card import Card, Suit, Rank


class TestHand(unittest.TestCase):
    """Tests for Hand class."""
    
    def test_empty_hand(self):
        """Test empty hand has score of 0."""
        hand = Hand()
        self.assertEqual(hand.get_score(), 0)
        self.assertEqual(len(hand.cards), 0)
    
    def test_add_card(self):
        """Test adding cards to hand."""
        hand = Hand()
        card = Card(Suit.HEARTS, Rank.ACE)
        hand.add_card(card)
        self.assertEqual(len(hand.cards), 1)
        self.assertEqual(hand.cards[0], card)
    
    def test_simple_score(self):
        """Test score calculation for simple hand."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.TWO))
        hand.add_card(Card(Suit.DIAMONDS, Rank.THREE))
        self.assertEqual(hand.get_score(), 5)
    
    def test_ace_as_11(self):
        """Test Ace counts as 11 when appropriate."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.KING))
        self.assertEqual(hand.get_score(), 21)
    
    def test_ace_as_1(self):
        """Test Ace counts as 1 to avoid bust."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.KING))
        hand.add_card(Card(Suit.DIAMONDS, Rank.TWO))
        self.assertEqual(hand.get_score(), 13)  # A=1, K=10, 2=2
    
    def test_multiple_aces(self):
        """Test multiple Aces handled correctly."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.ACE))
        self.assertEqual(hand.get_score(), 12)  # Both Aces = 11 + 1
    
    def test_is_bust(self):
        """Test bust detection."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.TEN))
        hand.add_card(Card(Suit.DIAMONDS, Rank.KING))
        hand.add_card(Card(Suit.CLUBS, Rank.TWO))
        self.assertTrue(hand.is_bust())
    
    def test_not_bust(self):
        """Test non-bust hand."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.TEN))
        hand.add_card(Card(Suit.DIAMONDS, Rank.FIVE))
        self.assertFalse(hand.is_bust())
    
    def test_is_blackjack(self):
        """Test blackjack detection."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.KING))
        self.assertTrue(hand.is_blackjack())
    
    def test_not_blackjack_three_cards(self):
        """Test 21 with 3 cards is not blackjack."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.SEVEN))
        hand.add_card(Card(Suit.DIAMONDS, Rank.SEVEN))
        hand.add_card(Card(Suit.CLUBS, Rank.SEVEN))
        self.assertFalse(hand.is_blackjack())
    
    def test_clear(self):
        """Test clearing hand."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.KING))
        hand.clear()
        self.assertEqual(len(hand.cards), 0)
        self.assertEqual(hand.get_score(), 0)
