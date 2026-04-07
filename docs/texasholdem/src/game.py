"""Main Texas Hold'em game engine."""

from typing import List, Optional, Tuple
from enum import Enum
import random

from .cards import Card, Deck, Suit, Rank
from .player import Player
from .hand_evaluator import HandEvaluator, HandResult
from .pot import Pot
from .betting import BettingRound, BettingAction


class GamePhase(Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    COMPLETE = "complete"


class TexasHoldemGame:
    """Main game engine for Texas Hold'em poker."""
    
    def __init__(self, small_blind: int = 10, big_blind: int = 20, seed: Optional[int] = None):
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.seed = seed
        self.rng = random.Random(seed) if seed is not None else random
        
        self.players: List[Player] = []
        self.deck: Optional[Deck] = None
        self.community_cards: List[Card] = []
        self.pot = Pot()
        self.phase = GamePhase.PREFLOP
        self.dealer_idx = 0
        self.current_betting_round: Optional[BettingRound] = None
        self.hand_history: List[str] = []
        self.winner: Optional[Player] = None
        self.winning_hand: Optional[HandResult] = None
    
    def add_player(self, name: str, chips: int, is_human: bool = False) -> Player:
        """Add a player to the game."""
        player = Player(name, chips, is_human)
        self.players.append(player)
        return player
    
    def start_hand(self) -> bool:
        """Start a new hand. Returns False if not enough players."""
        if len(self.players) < 2:
            return False
        
        # Check for players with chips
        active_players = [p for p in self.players if p.chips > 0]
        if len(active_players) < 2:
            return False
        
        # Reset state
        self.deck = Deck(self.seed)
        self.deck.shuffle()
        self.community_cards = []
        self.pot.reset()
        self.phase = GamePhase.PREFLOP
        self.winner = None
        self.winning_hand = None
        
        # Reset all players
        for player in self.players:
            player.reset_for_new_hand()
        
        # Set dealer and blinds
        self._set_blinds()
        
        # Deal hole cards
        self._deal_hole_cards()
        
        # Post blinds
        self._post_blinds()
        
        # Start preflop betting
        self._start_betting_round()
        
        return True
    
    def _set_blinds(self) -> None:
        """Set dealer button and blinds."""
        # Move dealer button
        self.dealer_idx = (self.dealer_idx + 1) % len(self.players)
        
        # Reset all positions
        for player in self.players:
            player.is_dealer = False
            player.is_small_blind = False
            player.is_big_blind = False
        
        # Set positions
        dealer = self.players[self.dealer_idx]
        dealer.is_dealer = True
        
        sb_idx = (self.dealer_idx + 1) % len(self.players)
        self.players[sb_idx].is_small_blind = True
        
        bb_idx = (self.dealer_idx + 2) % len(self.players)
        self.players[bb_idx].is_big_blind = True
    
    def _deal_hole_cards(self) -> None:
        """Deal two hole cards to each player."""
        for _ in range(2):
            for player in self.players:
                if player.chips > 0:  # Only deal to players with chips
                    card = self.deck.deal_one()
                    player.hand.append(card)
    
    def _post_blinds(self) -> None:
        """Post small and big blinds."""
        sb_player = next(p for p in self.players if p.is_small_blind)
        bb_player = next(p for p in self.players if p.is_big_blind)
        
        # Post small blind
        sb_amount = min(sb_player.chips, self.small_blind)
        sb_player.chips -= sb_amount
        sb_player.current_bet = sb_amount
        self.pot.add_chips(sb_player, sb_amount)
        
        # Post big blind
        bb_amount = min(bb_player.chips, self.big_blind)
        bb_player.chips -= bb_amount
        bb_player.current_bet = bb_amount
        self.pot.add_chips(bb_player, bb_amount)
    
    def _start_betting_round(self) -> None:
        """Start a new betting round."""
        active_players = [p for p in self.players if not p.folded and p.chips > 0]
        
        if len(active_players) <= 1:
            self._handle_fold_out()
            return
        
        # Find first active player after dealer (UTG)
        start_idx = (self.dealer_idx + 1) % len(self.players)
        for _ in range(len(self.players)):
            player = self.players[start_idx]
            if not player.folded and player.chips > 0:
                break
            start_idx = (start_idx + 1) % len(self.players)
        
        self.current_betting_round = BettingRound(
            players=self.players,
            pot=self.pot,
            min_bet=self.big_blind,
            max_bet=sum(p.chips + p.current_bet for p in self.players)
        )
        self.current_betting_round.next_player_idx = start_idx
        
        # Set current bet to big blind for preflop
        if self.phase == GamePhase.PREFLOP:
            self.current_betting_round.current_bet = self.big_blind
            # Mark big blind as having acted (their blind counts as an action)
            bb_player = next(p for p in self.players if p.is_big_blind)
            self.current_betting_round.actions_made[self.players.index(bb_player)] = True
        else:
            # For post-flop rounds, reset actions_made (new BettingRound already does this)
            pass
    
    def process_action(self, action: BettingAction, 
                       amount: Optional[int] = None) -> Tuple[bool, str]:
        """Process a player's betting action."""
        if not self.current_betting_round:
            return False, "No betting round active"
        
        success, message = self.current_betting_round.process_action(action, amount)
        
        if success:
            self.hand_history.append(message)
            
            # Check if round is complete
            if self.current_betting_round.round_complete:
                self._complete_betting_round()
        
        return success, message
    
    def _complete_betting_round(self) -> None:
        """Complete the current betting round and move to next phase."""
        # Check for fold-out winner
        if self.current_betting_round.all_but_one_folded:
            self.winner = self.current_betting_round.winner
            self.phase = GamePhase.COMPLETE
            return
        
        # Reset player bets for next round
        for player in self.players:
            player.current_bet = 0
        
        # Move to next phase
        if self.phase == GamePhase.PREFLOP:
            self.phase = GamePhase.FLOP
            self._deal_flop()
        elif self.phase == GamePhase.FLOP:
            self.phase = GamePhase.TURN
            self._deal_turn()
        elif self.phase == GamePhase.TURN:
            self.phase = GamePhase.RIVER
            self._deal_river()
        elif self.phase == GamePhase.RIVER:
            self.phase = GamePhase.SHOWDOWN
            self._showdown()
            return
        
        # Start next betting round
        self._start_betting_round()
    
    def _deal_flop(self) -> None:
        """Deal the flop (3 community cards)."""
        # Burn one card
        self.deck.deal_one()
        # Deal 3 cards
        for _ in range(3):
            self.community_cards.append(self.deck.deal_one())
    
    def _deal_turn(self) -> None:
        """Deal the turn (4th community card)."""
        self.deck.deal_one()  # Burn
        self.community_cards.append(self.deck.deal_one())
    
    def _deal_river(self) -> None:
        """Deal the river (5th community card)."""
        self.deck.deal_one()  # Burn
        self.community_cards.append(self.deck.deal_one())
    
    def _showdown(self) -> None:
        """Evaluate hands and determine winner(s)."""
        # Get active players with their best hands
        player_hands = []
        for player in self.players:
            if not player.folded:
                all_cards = player.hand + self.community_cards
                hand_result = HandEvaluator.evaluate(all_cards)
                player_hands.append((player, hand_result))
        
        # Sort by hand strength (descending)
        player_hands.sort(key=lambda x: (x[1].rank, x[1].tiebreaker), reverse=True)
        
        # Find all winners (may be split pot)
        best_hand = player_hands[0][1]
        winners = [p for p, h in player_hands if h == best_hand]
        
        # Distribute pot
        self.pot.distribute(winners)
        
        # Set winner info
        self.winner = winners[0] if len(winners) == 1 else None
        self.winning_hand = best_hand
        
        # Record results
        if len(winners) == 1:
            self.hand_history.append(f"{winners[0].name} wins with {best_hand.description}!")
        else:
            winner_names = ", ".join(w.name for w in winners)
            self.hand_history.append(f"Split pot between {winner_names} with {best_hand.description}!")
        
        self.phase = GamePhase.COMPLETE
    
    def _handle_fold_out(self) -> None:
        """Handle case where all but one player folded."""
        winner = next(p for p in self.players if not p.folded)
        self.pot.distribute([winner])
        self.winner = winner
        self.hand_history.append(f"{winner.name} wins by fold-out!")
        self.phase = GamePhase.COMPLETE
    
    def get_game_state(self) -> dict:
        """Get current game state as a dictionary."""
        return {
            "phase": self.phase.value,
            "dealer_idx": self.dealer_idx,
            "community_cards": [str(c) for c in self.community_cards],
            "pot_total": self.pot.get_total(),
            "players": [
                {
                    "name": p.name,
                    "chips": p.chips,
                    "hand": [str(c) for c in p.hand],
                    "folded": p.folded,
                    "all_in": p.all_in,
                    "is_dealer": p.is_dealer,
                    "is_small_blind": p.is_small_blind,
                    "is_big_blind": p.is_big_blind,
                    "current_bet": p.current_bet
                }
                for p in self.players
            ],
            "current_bettor": self.current_betting_round.get_current_player().name 
                if self.current_betting_round else None,
            "bet_info": self.current_betting_round.get_bet_info() 
                if self.current_betting_round else None
        }
    
    def is_game_complete(self) -> bool:
        """Check if the current hand is complete."""
        return self.phase == GamePhase.COMPLETE
    
    def get_winner_info(self) -> Optional[dict]:
        """Get information about the winner(s)."""
        if not self.winner and self.phase != GamePhase.COMPLETE:
            return None
        
        return {
            "winner": self.winner.name if self.winner else "Split",
            "hand": str(self.winning_hand) if self.winning_hand else None,
            "pot": self.pot.get_total()
        }
    
    def run(self, num_players: int = 4, auto_play: bool = True) -> None:
        """Run the game with automatic play.
        
        Args:
            num_players: Number of players to add (default 4)
            auto_play: If True, automatically play hands with AI decisions
        """
        # Add default players if none exist
        if not self.players:
            for i in range(num_players):
                self.add_player(f"Player {i+1}", chips=1000, is_human=False)
        
        print(f"\nStarting game with {len(self.players)} players...")
        print("="*60)
        
        hand_count = 0
        max_hands = 10  # Limit to 10 hands for demo
        
        while hand_count < max_hands:
            # Check if we have enough players
            active_players = [p for p in self.players if p.chips > 0]
            if len(active_players) < 2:
                print("\nNot enough players with chips remaining. Game over!")
                break
            
            hand_count += 1
            print(f"\n{'='*60}")
            print(f"HAND {hand_count}")
            print(f"{'='*60}")
            
            # Start a new hand
            if not self.start_hand():
                print("Could not start hand.")
                break
            
            # Print initial state
            self._print_game_state()
            
            # Auto-play the hand
            if auto_play:
                self._auto_play_hand()
            
            # Print results
            if self.is_game_complete():
                winner_info = self.get_winner_info()
                if winner_info:
                    print(f"\nWinner: {winner_info['winner']}")
                    if winner_info['hand']:
                        print(f"Hand: {winner_info['hand']}")
                    print(f"Pot: ${winner_info['pot']}")
            
            # Check if game should continue
            active_players = [p for p in self.players if p.chips > 0]
            if len(active_players) < 2:
                print("\nGame over - not enough players with chips!")
                break
            
            # Ask if user wants to continue (for now, just continue)
            if hand_count < max_hands:
                try:
                    print("\nPress Enter to continue to next hand...")
                    input()
                except EOFError:
                    # Non-interactive mode, just continue
                    pass
        
        print("\n" + "="*60)
        print("GAME OVER")
        print("="*60)
        
        # Print final standings
        print("\nFinal Standings:")
        for player in sorted(self.players, key=lambda p: p.chips, reverse=True):
            print(f"  {player.name}: ${player.chips}")
    
    def _print_game_state(self) -> None:
        """Print the current game state."""
        state = self.get_game_state()
        
        print(f"\nPhase: {state['phase'].upper()}")
        print(f"Community Cards: {', '.join(state['community_cards']) if state['community_cards'] else 'None'}")
        print(f"Pot: ${state['pot_total']}")
        print("\nPlayers:")
        
        for p in state['players']:
            position = ""
            if p['is_dealer']: position += " [D]"
            if p['is_small_blind']: position += " [SB]"
            if p['is_big_blind']: position += " [BB]"
            
            status = ""
            if p['folded']: status = " (FOLDED)"
            elif p['all_in']: status = " (ALL-IN)"
            
            hand_str = ""
            if not p['folded'] and p['hand']:
                hand_str = f" {', '.join(p['hand'])}"
            
            print(f"  {p['name']}{position}: ${p['chips']}{hand_str}{status}")
    
    def _auto_play_hand(self) -> None:
        """Automatically play through a hand with AI decisions."""
        while not self.is_game_complete():
            if not self.current_betting_round:
                break
            
            current_player = self.current_betting_round.get_current_player()
            if not current_player or current_player.folded or current_player.all_in:
                # Move to next player or complete round
                self.current_betting_round.advance_player()
                if self.current_betting_round.round_complete:
                    self._complete_betting_round()
                continue
            
            # Make an AI decision
            action, amount = self._make_ai_decision(current_player)
            
            success, message = self.process_action(action, amount)
            if success:
                print(f"  {current_player.name}: {message}")
                
                if self.current_betting_round.round_complete:
                    self._complete_betting_round()
                    if not self.is_game_complete():
                        self._print_game_state()
            else:
                print(f"  Error: {message}")
                break
    
    def _make_ai_decision(self, player: Player) -> Tuple[BettingAction, Optional[int]]:
        """Make a simple AI decision for a player.
        
        Returns:
            Tuple of (BettingAction, amount) where amount is None for check/fold/call
        """
        from .betting import BettingAction
        
        # Get current bet info
        bet_info = self.current_betting_round.get_bet_info()
        current_bet = bet_info['current_bet']
        player_bet = player.current_bet
        call_amount = current_bet - player_bet
        
        # Simple AI logic based on hand strength and position
        # For now, use random decisions with some basic logic
        
        # Evaluate hand strength (simple heuristic)
        hand_strength = self._evaluate_hand_strength(player)
        
        # Decision making
        if call_amount == 0:
            # Can check or bet
            if hand_strength > 0.7:
                # Strong hand - bet
                bet_amount = min(player.chips, self.big_blind * 2)
                return BettingAction.BET, bet_amount
            elif hand_strength > 0.4:
                # Medium hand - sometimes bet
                if self.rng.random() < 0.3:
                    bet_amount = min(player.chips, self.big_blind)
                    return BettingAction.BET, bet_amount
            # Otherwise check
            return BettingAction.CHECK, None
        else:
            # Need to call, raise, or fold
            if hand_strength > 0.8:
                # Very strong hand - raise
                raise_amount = min(player.chips, current_bet * 2)
                return BettingAction.RAISE, raise_amount
            elif hand_strength > 0.5:
                # Decent hand - call
                return BettingAction.CALL, None
            elif hand_strength > 0.2:
                # Weak hand - sometimes call, sometimes fold
                if self.rng.random() < 0.3:
                    return BettingAction.CALL, None
            # Fold
            return BettingAction.FOLD, None
    
    def _evaluate_hand_strength(self, player: Player) -> float:
        """Evaluate hand strength on a scale of 0.0 to 1.0.
        
        This is a simple heuristic for AI decision making.
        """
        if len(player.hand) < 2:
            return 0.0
        
        all_cards = player.hand + self.community_cards
        hand_result = HandEvaluator.evaluate(all_cards)
        
        # Map hand rank to strength (0.0 to 1.0)
        # Higher rank values are better hands
        rank_strength = {
            0: 0.1,   # High card
            1: 0.2,   # Pair
            2: 0.35,  # Two pair
            3: 0.5,   # Three of a kind
            4: 0.6,   # Straight
            5: 0.7,   # Flush
            6: 0.8,   # Full house
            7: 0.9,   # Four of a kind
            8: 1.0,   # Straight flush
        }
        
        base_strength = rank_strength.get(hand_result.rank, 0.1)
        
        # Add some randomness
        return base_strength + self.rng.uniform(-0.05, 0.05)
