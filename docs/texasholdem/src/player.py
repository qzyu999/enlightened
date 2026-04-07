"""Player class and related functionality."""

from typing import List, Optional
from .cards import Card


class Player:
    """Represents a player in the Texas Hold'em game."""
    
    def __init__(self, name: str, chips: int, is_human: bool = False):
        self.name = name
        self.chips = chips
        self.is_human = is_human
        self.hand: List[Card] = []
        self.folded = False
        self.all_in = False
        self.current_bet = 0  # Bet in current round
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False
    
    def deal_hand(self, cards: List[Card]) -> None:
        """Deal cards to this player."""
        self.hand = cards
    
    def reset_for_new_hand(self) -> None:
        """Reset player state for a new hand."""
        self.hand = []
        self.folded = False
        self.all_in = False
        self.current_bet = 0
        self.is_small_blind = False
        self.is_big_blind = False
    
    def can_call(self, amount: int) -> bool:
        """Check if player can call the given amount."""
        needed = amount - self.current_bet
        return self.chips >= needed
    
    def can_raise(self, amount: int) -> bool:
        """Check if player can raise to the given amount."""
        needed = amount - self.current_bet
        return self.chips >= needed
    
    def call(self, current_bet: int) -> int:
        """
        Call the current bet.
        Returns the amount called.
        """
        if self.all_in:
            return 0
        
        amount_to_call = current_bet - self.current_bet
        if amount_to_call <= 0:
            return 0
        
        if self.chips <= amount_to_call:
            # Go all-in
            amount = self.chips
            self.chips = 0
            self.all_in = True
        else:
            amount = amount_to_call
            self.chips -= amount
        
        self.current_bet += amount
        return amount
    
    def raise_bet(self, amount: int) -> int:
        """
        Raise to the given total amount.
        Returns the amount raised.
        """
        if self.all_in:
            return 0
        
        amount_to_add = amount - self.current_bet
        if amount_to_add <= 0:
            return 0
        
        if self.chips <= amount_to_add:
            # Go all-in
            amount = self.chips
            self.chips = 0
            self.all_in = True
        else:
            amount = amount_to_add
            self.chips -= amount
        
        self.current_bet += amount
        return amount
    
    def fold(self) -> None:
        """Fold the current hand."""
        self.folded = True
    
    def check(self) -> int:
        """
        Check (call with 0 if no bet to match).
        Returns amount added to pot.
        """
        return self.call(self.current_bet)
    
    def get_action_description(self, action: str, amount: int = 0) -> str:
        """Get a human-readable description of an action."""
        if action == "fold":
            return f"{self.name} folds"
        elif action == "check":
            return f"{self.name} checks"
        elif action == "call":
            if amount == 0:
                return f"{self.name} checks"
            return f"{self.name} calls ${amount}"
        elif action == "raise":
            return f"{self.name} raises to ${amount}"
        return f"{self.name} {action}"
    
    def __repr__(self) -> str:
        status = []
        if self.folded:
            status.append("FOLDED")
        if self.all_in:
            status.append("ALL-IN")
        if self.is_dealer:
            status.append("DEALER")
        if self.is_small_blind:
            status.append("SB")
        if self.is_big_blind:
            status.append("BB")
        
        status_str = " " + " ".join(status) if status else ""
        return f"Player({self.name}: ${self.chips}){status_str}"
