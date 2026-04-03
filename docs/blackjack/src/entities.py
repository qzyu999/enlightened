"""Player and Dealer classes for Blackjack game."""
from src.hand import Hand


class Player:
    """Represents a player in the game."""
    
    def __init__(self, name: str, chips: int = 100):
        self.name = name
        self.chips = chips
        self.hand = Hand()
        self.current_bet = 0
    
    def place_bet(self, amount: int) -> bool:
        """Place a bet. Returns True if successful."""
        if amount <= 0:
            return False
        if amount > self.chips:
            return False
        self.chips -= amount
        self.current_bet = amount
        return True
    
    def win_bet(self) -> None:
        """Return bet plus winnings."""
        self.chips += self.current_bet * 2
        self.current_bet = 0
    
    def push_bet(self) -> None:
        """Return bet (push/tie)."""
        self.chips += self.current_bet
        self.current_bet = 0
    
    def lose_bet(self) -> None:
        """Lose the current bet."""
        self.current_bet = 0
    
    def reset_hand(self) -> None:
        """Clear hand for new round."""
        self.hand.clear()
    
    def __str__(self) -> str:
        return f"{self.name} (${self.chips})"


class Dealer:
    """Represents the dealer."""
    
    def __init__(self):
        self.hand = Hand()
    
    def must_hit(self) -> bool:
        """Dealer must hit on soft 17."""
        return self.hand.get_score() < 17
    
    def reset_hand(self) -> None:
        """Clear hand for new round."""
        self.hand.clear()
    
    def __str__(self) -> str:
        return f"Dealer"
