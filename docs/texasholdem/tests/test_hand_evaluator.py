"""Unit tests for hand evaluation."""

import pytest
import sys
sys.path.insert(0, '/workspace')

from src.cards import Card, Suit, Rank, Deck
from src.hand_evaluator import (
    HandEvaluator, HandResult,
    ROYAL_FLUSH, STRAIGHT_FLUSH, FOUR_OF_A_KIND,
    FULL_HOUSE, FLUSH, STRAIGHT, THREE_OF_A_KIND,
    TWO_PAIR, ONE_PAIR, HIGH_CARD
)


def make_card(rank: Rank, suit: Suit) -> Card:
    return Card(suit, rank)


class TestHandEvaluator:
    # HIGH CARD TESTS
    def test_high_card(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.JACK, Suit.CLUBS),
            make_card(Rank.NINE, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HIGH_CARD
        assert result.description == "High Card"
        assert result.tiebreaker[0] == 14  # Ace high
    
    def test_high_card_comparison(self):
        hand1 = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.JACK, Suit.CLUBS),
            make_card(Rank.NINE, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        hand2 = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.JACK, Suit.CLUBS),
            make_card(Rank.EIGHT, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result1 = HandEvaluator.evaluate(hand1)
        result2 = HandEvaluator.evaluate(hand2)
        assert result1 > result2  # 9-high kicker beats 8-high

    # ONE PAIR TESTS
    def test_one_pair(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == ONE_PAIR
        assert result.description == "One Pair"
        assert result.tiebreaker[0] == 14  # Pair of Aces
    
    def test_one_pair_comparison(self):
        pair_aces = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        pair_kings = [
            make_card(Rank.KING, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.ACE, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result1 = HandEvaluator.evaluate(pair_aces)
        result2 = HandEvaluator.evaluate(pair_kings)
        assert result1 > result2  # Pair of Aces beats Pair of Kings

    # TWO PAIR TESTS
    def test_two_pair(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.KING, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == TWO_PAIR
        assert result.description == "Two Pair"
        assert result.tiebreaker[0] == 14  # Aces
        assert result.tiebreaker[1] == 13  # Kings
    
    def test_two_pair_comparison(self):
        aces_kings = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.KING, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        aces_queens = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.QUEEN, Suit.CLUBS),
            make_card(Rank.QUEEN, Suit.SPADES),
            make_card(Rank.KING, Suit.HEARTS)
        ]
        result1 = HandEvaluator.evaluate(aces_kings)
        result2 = HandEvaluator.evaluate(aces_queens)
        assert result1 > result2  # Aces-Kings beats Aces-Queens

    # THREE OF A KIND TESTS
    def test_three_of_a_kind(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.ACE, Suit.CLUBS),
            make_card(Rank.KING, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == THREE_OF_A_KIND
        assert result.description == "Three of a Kind"
        assert result.tiebreaker[0] == 14  # Three Aces

    # STRAIGHT TESTS
    def test_straight(self):
        cards = [
            make_card(Rank.FIVE, Suit.HEARTS),
            make_card(Rank.FOUR, Suit.DIAMONDS),
            make_card(Rank.THREE, Suit.CLUBS),
            make_card(Rank.TWO, Suit.SPADES),
            make_card(Rank.SIX, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == STRAIGHT
        assert result.description == "Straight"
        assert result.tiebreaker[0] == 6  # 6-high straight
    
    def test_straight_ace_low(self):
        """Test wheel straight (A-2-3-4-5)."""
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.FIVE, Suit.DIAMONDS),
            make_card(Rank.FOUR, Suit.CLUBS),
            make_card(Rank.THREE, Suit.SPADES),
            make_card(Rank.TWO, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == STRAIGHT
        assert result.description == "Straight"
        assert result.tiebreaker[0] == 5  # 5-high (wheel)
    
    def test_straight_ace_high(self):
        """Test Broadway straight (10-J-Q-K-A)."""
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.QUEEN, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.TEN, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == STRAIGHT
        assert result.description == "Straight"
        assert result.tiebreaker[0] == 14  # Ace-high

    # FLUSH TESTS
    def test_flush(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.HEARTS),
            make_card(Rank.JACK, Suit.HEARTS),
            make_card(Rank.NINE, Suit.HEARTS),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == FLUSH
        assert result.description == "Flush"

    # FULL HOUSE TESTS
    def test_full_house(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.ACE, Suit.CLUBS),
            make_card(Rank.KING, Suit.SPADES),
            make_card(Rank.KING, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == FULL_HOUSE
        assert result.description == "Full House"
        assert result.tiebreaker[0] == 14  # Three Aces
        assert result.tiebreaker[1] == 13  # Two Kings

    # FOUR OF A KIND TESTS
    def test_four_of_a_kind(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.ACE, Suit.CLUBS),
            make_card(Rank.ACE, Suit.SPADES),
            make_card(Rank.KING, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == FOUR_OF_A_KIND
        assert result.description == "Four of a Kind"
        assert result.tiebreaker[0] == 14  # Four Aces

    # STRAIGHT FLUSH TESTS
    def test_straight_flush(self):
        cards = [
            make_card(Rank.NINE, Suit.HEARTS),
            make_card(Rank.EIGHT, Suit.HEARTS),
            make_card(Rank.SEVEN, Suit.HEARTS),
            make_card(Rank.SIX, Suit.HEARTS),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == STRAIGHT_FLUSH
        assert result.description == "Straight Flush"
        assert result.tiebreaker[0] == 9  # 9-high

    # ROYAL FLUSH TESTS
    def test_royal_flush(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.HEARTS),
            make_card(Rank.QUEEN, Suit.HEARTS),
            make_card(Rank.JACK, Suit.HEARTS),
            make_card(Rank.TEN, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == ROYAL_FLUSH
        assert result.description == "Royal Flush"

    # SEVEN CARD EVALUATION (2 hole + 5 community)
    def test_best_five_from_seven(self):
        """Test that evaluator picks best 5 from 7 cards."""
        # Player has pocket Aces, board has flush
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),      # Hole
            make_card(Rank.ACE, Suit.DIAMONDS),    # Hole
            make_card(Rank.KING, Suit.CLUBS),      # Board
            make_card(Rank.JACK, Suit.SPADES),     # Board
            make_card(Rank.TEN, Suit.HEARTS),      # Board
            make_card(Rank.NINE, Suit.HEARTS),     # Board
            make_card(Rank.EIGHT, Suit.HEARTS)     # Board
        ]
        result = HandEvaluator.evaluate(cards)
        # Should pick pair of Aces (not the flush)
        assert result.rank == ONE_PAIR
        assert result.tiebreaker[0] == 14

    def test_straight_from_seven_cards(self):
        """Test finding straight among 7 cards."""
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.QUEEN, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.TEN, Suit.HEARTS),
            make_card(Rank.FIVE, Suit.DIAMONDS),
            make_card(Rank.THREE, Suit.CLUBS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == STRAIGHT
        assert result.tiebreaker[0] == 14  # Broadway

    # HAND COMPARISON
    def test_compare_hands(self):
        hand1 = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        hand2 = [
            make_card(Rank.KING, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.ACE, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        
        result = HandEvaluator.compare_hands(hand1, hand2)
        assert result > 0  # Hand 1 wins

    def test_compare_identical_hands(self):
        cards1 = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.JACK, Suit.CLUBS),
            make_card(Rank.NINE, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        cards2 = [
            make_card(Rank.ACE, Suit.SPADES),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.JACK, Suit.HEARTS),
            make_card(Rank.NINE, Suit.DIAMONDS),
            make_card(Rank.FIVE, Suit.SPADES)
        ]
        
        result = HandEvaluator.compare_hands(cards1, cards2)
        assert result == 0  # Tie

    # EDGE CASES
    def test_insufficient_cards(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS)
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == -1
        assert result.description == "Insufficient cards"

    def test_hand_result_repr(self):
        cards = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        result = HandEvaluator.evaluate(cards)
        repr_str = repr(result)
        assert "One Pair" in repr_str
        assert "rank=100" in repr_str
