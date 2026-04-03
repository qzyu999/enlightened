"""Deck module for Blackjack game."""
import random
from typing import List
from src.card import Card, Suit, Rank


class Deck:
    """Represents a standard 52-card deck."""
    
    def __init__(self):
        """Initialize a new deck with 52 cards."""
        self.cards: List[Card] = []
        self._build_deck()
    
    def _build_deck(self) -> None:
        """Build a complete deck of 52 cards."""
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self) -> None:
        """Shuffle the deck using Fisher-Yates algorithm."""
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        """Deal the top card from the deck."""
        if not self.cards:
            raise IndexError("Cannot deal from empty deck")
        return self.cards.pop()
    
    def remaining(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards)
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        return f"Deck({len(self.cards)} cards remaining)"
