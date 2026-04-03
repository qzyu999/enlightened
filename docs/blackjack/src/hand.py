"""Hand module for Blackjack game."""
from typing import List
from src.card import Card


class Hand:
    """Represents a player's or dealer's hand."""
    
    def __init__(self):
        """Initialize an empty hand."""
        self.cards: List[Card] = []
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)
    
    def get_score(self) -> int:
        """Calculate hand score with proper Ace handling."""
        score = 0
        ace_count = 0
        
        for card in self.cards:
            if card.rank.name == "ACE":
                ace_count += 1
                score += 11
            else:
                score += card.value
        
        # Adjust for aces if bust
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1
        
        return score
    
    def is_bust(self) -> bool:
        """Check if hand has busted (over 21)."""
        return self.get_score() > 21
    
    def is_blackjack(self) -> bool:
        """Check if hand is a natural blackjack (Ace + 10-value card)."""
        if len(self.cards) != 2:
            return False
        values = [card.value for card in self.cards]
        return 11 in values and 10 in values
    
    def clear(self) -> None:
        """Clear all cards from the hand."""
        self.cards.clear()
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] = {self.get_score()}"
    
    def __repr__(self) -> str:
        return f"Hand(cards={self.cards}, score={self.get_score()})"
