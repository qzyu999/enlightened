"""Unit tests for Deck module."""
import unittest
import sys
sys.path.insert(0, '.')
from src.deck import Deck
from src.card import Suit, Rank


class TestDeck(unittest.TestCase):
    """Tests for Deck class."""
    
    def test_deck_creation(self):
        """Test deck is created with 52 cards."""
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)
    
    def test_deck_has_all_suits_and_ranks(self):
        """Test deck contains all combinations."""
        deck = Deck()
        suits = set(card.suit for card in deck.cards)
        ranks = set(card.rank for card in deck.cards)
        self.assertEqual(len(suits), 4)
        self.assertEqual(len(ranks), 13)
    
    def test_shuffle_changes_order(self):
        """Test that shuffle changes card order."""
        deck1 = Deck()
        deck2 = Deck()
        deck2.shuffle()
        self.assertNotEqual(deck1.cards, deck2.cards)
    
    def test_deal_returns_card(self):
        """Test dealing returns a card."""
        deck = Deck()
        card = deck.deal()
        self.assertIsNotNone(card)
    
    def test_deal_reduces_count(self):
        """Test dealing reduces remaining cards."""
        deck = Deck()
        initial = deck.remaining()
        deck.deal()
        self.assertEqual(deck.remaining(), initial - 1)
    
    def test_deal_all_cards(self):
        """Test dealing all cards."""
        deck = Deck()
        dealt = []
        while deck.remaining() > 0:
            dealt.append(deck.deal())
        self.assertEqual(len(dealt), 52)
    
    def test_deal_from_empty_deck(self):
        """Test dealing from empty deck raises IndexError."""
        deck = Deck()
        while deck.remaining() > 0:
            deck.deal()
        with self.assertRaises(IndexError):
            deck.deal()
    
    def test_remaining_after_deals(self):
        """Test remaining count after multiple deals."""
        deck = Deck()
        for _ in range(10):
            deck.deal()
        self.assertEqual(deck.remaining(), 42)
