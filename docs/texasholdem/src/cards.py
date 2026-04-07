"""Card, Suit, Rank, and Deck implementations for Texas Hold'em."""

from enum import Enum
from typing import List, Optional
import random


class Suit(Enum):
    """Card suits with display characters."""
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"
    
    def is_red(self) -> bool:
        return self in (Suit.HEARTS, Suit.DIAMONDS)


class Rank(Enum):
    """Card ranks with numeric values for comparison."""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card:
    """Represents a single playing card."""
    
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self) -> str:
        rank_char = {
            Rank.TWO: "2", Rank.THREE: "3", Rank.FOUR: "4",
            Rank.FIVE: "5", Rank.SIX: "6", Rank.SEVEN: "7",
            Rank.EIGHT: "8", Rank.NINE: "9", Rank.TEN: "T",
            Rank.JACK: "J", Rank.QUEEN: "Q", Rank.KING: "K", Rank.ACE: "A"
        }
        return f"{rank_char[self.rank]}{self.suit.value}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self) -> int:
        return hash((self.suit, self.rank))
    
    def __lt__(self, other: 'Card') -> bool:
        if self.rank.value != other.rank.value:
            return self.rank.value < other.rank.value
        return self.suit.value < other.suit.value


class Deck:
    """Standard 52-card deck with shuffling capabilities."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize deck with optional seed for reproducibility."""
        self.seed = seed
        self.rng = random.Random(seed) if seed is not None else random
        self.cards: List[Card] = []
        self._build()
    
    def _build(self) -> None:
        """Build a complete 52-card deck."""
        self.cards = [
            Card(suit, rank) 
            for suit in Suit 
            for rank in Rank
        ]
    
    def shuffle(self) -> 'Deck':
        """Shuffle the deck in place."""
        self.rng.shuffle(self.cards)
        return self
    
    def deal(self, count: int = 1) -> List[Card]:
        """Deal specified number of cards from top of deck."""
        if count > len(self.cards):
            raise ValueError(f"Cannot deal {count} cards, only {len(self.cards)} remain")
        dealt = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt
    
    def deal_one(self) -> Card:
        """Deal a single card."""
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop(0)
    
    def remaining(self) -> int:
        """Return number of cards remaining in deck."""
        return len(self.cards)
    
    def reset(self) -> 'Deck':
        """Reset deck to full 52 cards."""
        self._build()
        return self
