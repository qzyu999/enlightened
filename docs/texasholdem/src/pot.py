"""Pot and side pot management for Texas Hold'em."""

from typing import List, Tuple
from .player import Player


class Pot:
    """Manages the main pot and side pots."""
    
    def __init__(self):
        self.main_pot = 0
        self.side_pots: List[Tuple[int, List[Player]]] = []  # (amount, eligible_players)
    
    def add_chips(self, player: Player, amount: int) -> None:
        """Add chips to the appropriate pot."""
        if amount <= 0:
            return
        
        # Find the highest pot this player can contribute to
        for side_pot in reversed(self.side_pots):
            if player in side_pot[1]:
                side_pot_amount, _ = side_pot
                side_pot[0] = side_pot_amount + amount
                return
        
        # Add to main pot
        self.main_pot += amount
    
    def create_side_pot(self, amount: int, eligible_players: List[Player]) -> None:
        """Create a new side pot."""
        self.side_pots.append((amount, eligible_players))
    
    def get_total(self) -> int:
        """Get total chips in all pots."""
        total = self.main_pot
        for side_pot, _ in self.side_pots:
            total += side_pot
        return total
    
    def get_eligible_pots(self, player: Player) -> List[Tuple[int, List[Player]]]:
        """Get all pots a player is eligible to win."""
        pots = []
        
        # Check side pots
        for side_pot_amount, eligible_players in self.side_pots:
            if player in eligible_players:
                pots.append((side_pot_amount, eligible_players))
        
        # Main pot is always eligible
        all_players = set()
        for _, eligible in self.side_pots:
            all_players.update(eligible)
        
        return pots + [(self.main_pot, list(all_players))]
    
    def distribute(self, winners: List[Player]) -> None:
        """
        Distribute pots to winners.
        Winners should be sorted by hand strength (best first).
        """
        if not winners:
            return
        
        # Distribute side pots first (highest pots first)
        for side_pot_amount, eligible_players in reversed(self.side_pots):
            eligible_winners = [w for w in winners if w in eligible_players]
            if eligible_winners:
                self._split_pot(side_pot_amount, eligible_winners)
        
        # Distribute main pot
        self._split_pot(self.main_pot, winners)
        
        # Reset pots
        self.main_pot = 0
        self.side_pots = []
    
    def _split_pot(self, amount: int, winners: List[Player]) -> None:
        """Split a pot evenly among winners."""
        if not winners:
            return
        
        per_player = amount // len(winners)
        remainder = amount % len(winners)
        
        for i, player in enumerate(winners):
            chips = per_player + (1 if i < remainder else 0)
            player.chips += chips
    
    def reset(self) -> None:
        """Reset all pots."""
        self.main_pot = 0
        self.side_pots = []
    
    def __repr__(self) -> str:
        pots_str = f"Main: ${self.main_pot}"
        if self.side_pots:
            for i, (amount, _) in enumerate(self.side_pots):
                pots_str += f", Side{i+1}: ${amount}"
        return f"Pot({pots_str})"
