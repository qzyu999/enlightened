"""Unit tests for card operations."""

import pytest
import sys
sys.path.insert(0, '/workspace')

from src.cards import Card, Suit, Rank, Deck


class TestSuit:
    def test_suit_values(self):
        assert len(list(Suit)) == 4
        assert Suit.HEARTS.is_red() == True
        assert Suit.DIAMONDS.is_red() == True
        assert Suit.CLUBS.is_red() == False
        assert Suit.SPADES.is_red() == False


class TestRank:
    def test_rank_values(self):
        assert len(list(Rank)) == 13
        assert Rank.TWO.value == 2
        assert Rank.TEN.value == 10
        assert Rank.JACK.value == 11
        assert Rank.QUEEN.value == 12
        assert Rank.KING.value == 13
        assert Rank.ACE.value == 14


class TestCard:
    def test_card_creation(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        assert card.suit == Suit.HEARTS
        assert card.rank == Rank.ACE
    
    def test_card_repr(self):
        card = Card(Suit.HEARTS, Rank.ACE)
        assert str(card) == "A♥"
        
        card2 = Card(Suit.SPADES, Rank.TEN)
        assert str(card2) == "T♠"
        
        card3 = Card(Suit.CLUBS, Rank.KING)
        assert str(card3) == "K♣"
    
    def test_card_equality(self):
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.HEARTS, Rank.ACE)
        card3 = Card(Suit.SPADES, Rank.ACE)
        
        assert card1 == card2
        assert card1 != card3
    
    def test_card_hash(self):
        card1 = Card(Suit.HEARTS, Rank.ACE)
        card2 = Card(Suit.HEARTS, Rank.ACE)
        
        assert hash(card1) == hash(card2)
        
        # Can be used in sets
        card_set = {card1, card2, Card(Suit.SPADES, Rank.KING)}
        assert len(card_set) == 2
    
    def test_card_comparison(self):
        ace_hearts = Card(Suit.HEARTS, Rank.ACE)
        ace_spades = Card(Suit.SPADES, Rank.ACE)
        king_hearts = Card(Suit.HEARTS, Rank.KING)
        
        assert ace_hearts > king_hearts
        assert ace_spades > king_hearts
        # Same rank, compare by suit
        assert ace_spades > ace_hearts


class TestDeck:
    def test_deck_creation(self):
        deck = Deck()
        assert len(deck.cards) == 52
    
    def test_deck_has_all_cards(self):
        deck = Deck()
        suits = set(c.suit for c in deck.cards)
        ranks = set(c.rank for c in deck.cards)
        
        assert suits == set(Suit)
        assert ranks == set(Rank)
    
    def test_deck_shuffle(self):
        deck1 = Deck(seed=42)
        deck1.shuffle()
        cards1 = deck1.cards.copy()
        
        deck2 = Deck(seed=42)
        deck2.shuffle()
        
        assert cards1 == deck2.cards
    
    def test_deck_deal(self):
        deck = Deck(seed=123)
        deck.shuffle()
        
        dealt = deck.deal(5)
        assert len(dealt) == 5
        assert len(deck.cards) == 47
    
    def test_deck_deal_one(self):
        deck = Deck(seed=456)
        deck.shuffle()
        
        card = deck.deal_one()
        assert isinstance(card, Card)
        assert len(deck.cards) == 51
    
    def test_deck_deal_all(self):
        deck = Deck()
        all_cards = deck.deal(52)
        assert len(all_cards) == 52
        assert deck.remaining() == 0
    
    def test_deck_deal_too_many(self):
        deck = Deck()
        with pytest.raises(ValueError):
            deck.deal(53)
    
    def test_deck_deal_one_empty(self):
        deck = Deck()
        deck.deal(52)
        with pytest.raises(ValueError):
            deck.deal_one()
    
    def test_deck_remaining(self):
        deck = Deck()
        assert deck.remaining() == 52
        deck.deal(10)
        assert deck.remaining() == 42
    
    def test_deck_reset(self):
        deck = Deck()
        deck.deal(10)
        deck.reset()
        assert len(deck.cards) == 52
    
    def test_deterministic_shuffling(self):
        """Test that same seed produces same shuffle."""
        seeds = [1, 42, 12345, 999999]
        
        for seed in seeds:
            deck1 = Deck(seed=seed)
            deck1.shuffle()
            order1 = [str(c) for c in deck1.cards]
            
            deck2 = Deck(seed=seed)
            deck2.shuffle()
            order2 = [str(c) for c in deck2.cards]
            
            assert order1 == order2, f"Seed {seed} produced different orders"
