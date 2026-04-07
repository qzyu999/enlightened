"""Betting round management for Texas Hold'em."""

from typing import List, Optional, Tuple
from enum import Enum
from .player import Player
from .pot import Pot


class BettingAction(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"


class BettingRound:
    """Manages a single betting round."""
    
    def __init__(self, players: List[Player], pot: Pot, 
                 min_bet: int, max_bet: Optional[int] = None):
        self.players = players
        self.pot = pot
        self.min_bet = min_bet
        self.max_bet = max_bet or float('inf')
        
        self.current_bet = 0  # Current bet to match
        self.next_player_idx = 0
        self.last_raiser_idx = -1
        self.round_complete = False
        self.all_but_one_folded = False
        self.winner: Optional[Player] = None
        
        # Track if everyone has had a chance to act
        self.actions_made: List[bool] = [False] * len(players)
        self.first_action_made = False
    
    def get_active_players(self) -> List[Player]:
        """Get players who haven't folded or gone all-in."""
        return [p for p in self.players if not p.folded and not p.all_in]
    
    def get_current_player(self) -> Optional[Player]:
        """Get the current player whose turn it is."""
        active = self.get_active_players()
        if not active:
            return None
        
        # Find next active player without modifying next_player_idx
        search_idx = self.next_player_idx
        for _ in range(len(self.players)):
            player = self.players[search_idx]
            if not player.folded and not player.all_in:
                return player
            search_idx = (search_idx + 1) % len(self.players)
        
        return None
    
    def process_action(self, action: BettingAction, 
                       amount: Optional[int] = None) -> Tuple[bool, str]:
        """
        Process a player's action.
        Returns (success, message).
        """
        player = self.get_current_player()
        if not player:
            return False, "No current player"
        
        if action == BettingAction.FOLD:
            player.fold()
            self.actions_made[self.players.index(player)] = True
            self.first_action_made = True
            self.next_player_idx = (self.next_player_idx + 1) % len(self.players)
            self._check_fold_out()
            return True, f"{player.name} folds"
        
        elif action == BettingAction.CHECK:
            if self.current_bet > player.current_bet:
                return False, "Cannot check - must call first"
            self.actions_made[self.players.index(player)] = True
            self.first_action_made = True
            self.next_player_idx = (self.next_player_idx + 1) % len(self.players)
            self._check_round_complete()
            return True, f"{player.name} checks"
        
        elif action == BettingAction.CALL:
            amount_called = player.call(self.current_bet)
            self.pot.add_chips(player, amount_called)
            self.actions_made[self.players.index(player)] = True
            self.first_action_made = True
            self.next_player_idx = (self.next_player_idx + 1) % len(self.players)
            self._check_round_complete()
            return True, f"{player.name} calls ${amount_called}"
        
        elif action == BettingAction.RAISE:
            if amount is None:
                amount = self.current_bet + self.min_bet
            
            if amount < self.current_bet + self.min_bet:
                return False, f"Minimum raise is ${self.current_bet + self.min_bet}"
            
            if amount > self.max_bet:
                return False, f"Maximum bet is ${self.max_bet}"
            
            amount_raised = player.raise_bet(amount)
            self.pot.add_chips(player, amount_raised)
            self.current_bet = amount
            self.last_raiser_idx = self.players.index(player)
            self.actions_made[self.players.index(player)] = True
            self.first_action_made = True
            self.next_player_idx = (self.next_player_idx + 1) % len(self.players)
            
            # Reset actions for other players (they need to act again)
            for i, p in enumerate(self.players):
                if p != player and not p.folded and not p.all_in:
                    self.actions_made[i] = False
            
            return True, f"{player.name} raises to ${amount}"
        
        return False, "Invalid action"
    
    def _check_fold_out(self) -> None:
        """Check if all but one player has folded."""
        active_count = sum(1 for p in self.players if not p.folded)
        if active_count == 1:
            self.all_but_one_folded = True
            self.round_complete = True
            self.winner = next(p for p in self.players if not p.folded)
    
    def _check_round_complete(self) -> None:
        """Check if the betting round is complete."""
        if not self.first_action_made:
            return
        
        # Don't override if already complete due to fold-out
        if self.all_but_one_folded:
            return
        
        active_players = self.get_active_players()
        if not active_players:
            self.round_complete = True
            return
        
        # Check if everyone has acted and matched the bet
        all_matched = all(
            p.current_bet >= self.current_bet or p.all_in
            for p in active_players
        )
        
        all_acted = all(
            self.actions_made[self.players.index(p)] or p.all_in
            for p in active_players
        )
        
        # Round is complete if everyone has acted and matched
        if all_matched and all_acted:
            self.round_complete = True
    
    def get_valid_actions(self, player: Player) -> List[BettingAction]:
        """Get valid actions for a player."""
        actions = [BettingAction.FOLD]
        
        can_check = player.current_bet >= self.current_bet
        can_call = player.can_call(self.current_bet)
        can_raise = player.chips > 0
        
        if can_check:
            actions.append(BettingAction.CHECK)
        
        if can_call:
            actions.append(BettingAction.CALL)
        
        if can_raise and self.current_bet < self.max_bet:
            actions.append(BettingAction.RAISE)
        
        return actions
    
    def get_bet_info(self) -> dict:
        """Get current betting information."""
        return {
            "current_bet": self.current_bet,
            "to_call": self.current_bet - self.get_current_player().current_bet 
                       if self.get_current_player() else 0,
            "min_raise": self.current_bet + self.min_bet,
            "max_raise": self.max_bet
        }
