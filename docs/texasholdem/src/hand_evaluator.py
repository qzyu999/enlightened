"""Hand evaluation logic for Texas Hold'em poker."""

from typing import List, Tuple
from collections import Counter
from .cards import Card, Suit, Rank


# Hand ranking constants (higher = better)
ROYAL_FLUSH = 900
STRAIGHT_FLUSH = 800
FOUR_OF_A_KIND = 700
FULL_HOUSE = 600
FLUSH = 500
STRAIGHT = 400
THREE_OF_A_KIND = 300
TWO_PAIR = 200
ONE_PAIR = 100
HIGH_CARD = 0


class HandResult:
    """Represents the result of a hand evaluation."""
    
    def __init__(self, rank: int, description: str, tiebreaker: Tuple[int, ...]):
        self.rank = rank
        self.description = description
        self.tiebreaker = tiebreaker
    
    def __repr__(self) -> str:
        return f"{self.description} (rank={self.rank})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HandResult):
            return False
        return self.rank == other.rank and self.tiebreaker == other.tiebreaker
    
    def __lt__(self, other: 'HandResult') -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.tiebreaker < other.tiebreaker
    
    def __gt__(self, other: 'HandResult') -> bool:
        if self.rank != other.rank:
            return self.rank > other.rank
        return self.tiebreaker > other.tiebreaker
    
    def __le__(self, other: 'HandResult') -> bool:
        return self == other or self < other
    
    def __ge__(self, other: 'HandResult') -> bool:
        return self == other or self > other


class HandEvaluator:
    """Evaluates poker hands and determines rankings."""
    
    @staticmethod
    def evaluate(cards: List[Card]) -> HandResult:
        """
        Evaluate up to 7 cards (2 hole + 5 community) and return best 5-card hand.
        
        Args:
            cards: List of 2-7 cards to evaluate
            
        Returns:
            HandResult with rank, description, and tiebreaker values
        """
        if len(cards) < 5:
            return HandResult(-1, "Insufficient cards", tuple())
        
        # Try all combinations of 5 cards from available cards
        best_result = None
        
        from itertools import combinations
        for combo in combinations(cards, 5):
            result = HandEvaluator._evaluate_five_cards(list(combo))
            if best_result is None or result > best_result:
                best_result = result
        
        return best_result
    
    @staticmethod
    def _evaluate_five_cards(cards: List[Card]) -> HandResult:
        """Evaluate exactly 5 cards."""
        # Sort cards by rank value (descending)
        cards.sort(key=lambda c: c.rank.value, reverse=True)
        
        # Check for flush
        is_flush = HandEvaluator._is_flush(cards)
        
        # Check for straight
        straight_high = HandEvaluator._get_straight_high(cards)
        
        # Get rank counts
        rank_counts = Counter(c.rank.value for c in cards)
        
        # Check combinations in order of precedence
        if is_flush and straight_high:
            if straight_high == Rank.ACE.value and all(
                c.rank.value in (14, 13, 12, 11, 10) for c in cards
            ):
                return HandResult(ROYAL_FLUSH, "Royal Flush", (straight_high,))
            return HandResult(STRAIGHT_FLUSH, "Straight Flush", (straight_high,))
        
        if 4 in rank_counts.values():
            quad_rank = next(r for r, count in rank_counts.items() if count == 4)
            kicker = next(r for r, count in rank_counts.items() if count == 1)
            return HandResult(FOUR_OF_A_KIND, "Four of a Kind", (quad_rank, kicker))
        
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            triple_rank = next(r for r, count in rank_counts.items() if count == 3)
            pair_rank = next(r for r, count in rank_counts.items() if count == 2)
            return HandResult(FULL_HOUSE, "Full House", (triple_rank, pair_rank))
        
        if is_flush:
            high_cards = tuple(c.rank.value for c in cards)
            return HandResult(FLUSH, "Flush", high_cards)
        
        if straight_high:
            return HandResult(STRAIGHT, "Straight", (straight_high,))
        
        if 3 in rank_counts.values():
            triple_rank = next(r for r, count in rank_counts.items() if count == 3)
            kickers = sorted(
                (r for r, count in rank_counts.items() if count == 1),
                reverse=True
            )
            return HandResult(THREE_OF_A_KIND, "Three of a Kind", 
                           (triple_rank,) + tuple(kickers))
        
        pairs = [r for r, count in rank_counts.items() if count == 2]
        if len(pairs) >= 2:
            pairs.sort(reverse=True)
            kicker = next(r for r, count in rank_counts.items() if count == 1)
            return HandResult(TWO_PAIR, "Two Pair", (pairs[0], pairs[1], kicker))
        
        if len(pairs) == 1:
            pair_rank = pairs[0]
            kickers = sorted(
                (r for r, count in rank_counts.items() if count == 1),
                reverse=True
            )
            return HandResult(ONE_PAIR, "One Pair", (pair_rank,) + tuple(kickers))
        
        # High card
        high_cards = tuple(c.rank.value for c in cards)
        return HandResult(HIGH_CARD, "High Card", high_cards)
    
    @staticmethod
    def _is_flush(cards: List[Card]) -> bool:
        """Check if all cards are the same suit."""
        return len(set(c.suit for c in cards)) == 1
    
    @staticmethod
    def _get_straight_high(cards: List[Card]) -> int:
        """
        Check if cards form a straight and return high card value.
        Returns 0 if not a straight.
        """
        # Get unique rank values sorted descending
        unique_ranks = sorted(set(c.rank.value for c in cards), reverse=True)
        
        # Check for regular straight
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                return unique_ranks[i]
        
        # Check for wheel (A-2-3-4-5)
        if set(unique_ranks) >= {14, 5, 4, 3, 2}:
            return 5  # 5-high straight
        
        return 0
    
    @staticmethod
    def compare_hands(cards1: List[Card], cards2: List[Card]) -> int:
        """
        Compare two hands. Returns positive if hand1 wins,
        negative if hand2 wins, 0 for tie.
        """
        result1 = HandEvaluator.evaluate(cards1)
        result2 = HandEvaluator.evaluate(cards2)
        
        if result1 > result2:
            return 1
        elif result1 < result2:
            return -1
        return 0
