"""Game engine for Blackjack game."""
from src.deck import Deck
from src.entities import Player, Dealer
from typing import Optional


class GameEngine:
    """Manages game logic and flow."""
    
    def __init__(self):
        self.deck = Deck()
        self.player: Optional[Player] = None
        self.dealer: Optional[Dealer] = None
        self.game_over = False
    
    def setup(self, player_name: str = "Player", starting_chips: int = 100) -> None:
        """Initialize a new game."""
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player(player_name, starting_chips)
        self.dealer = Dealer()
        self.game_over = False
    
    def deal_initial_cards(self) -> None:
        """Deal two cards to player and dealer."""
        self.player.hand.add_card(self.deck.deal())
        self.dealer.hand.add_card(self.deck.deal())
        self.player.hand.add_card(self.deck.deal())
        self.dealer.hand.add_card(self.deck.deal())
    
    def player_hit(self) -> None:
        """Player takes another card."""
        self.player.hand.add_card(self.deck.deal())
    
    def player_stand(self) -> None:
        """Player stands, dealer plays out hand."""
        while self.dealer.must_hit():
            self.dealer.hand.add_card(self.deck.deal())
    
    def get_winner(self) -> str:
        """Determine the winner. Returns 'player', 'dealer', or 'push'."""
        player_score = self.player.hand.get_score()
        dealer_score = self.dealer.hand.get_score()
        
        if player_score > 21:
            return "dealer"
        if dealer_score > 21:
            return "player"
        if player_score > dealer_score:
            return "player"
        if dealer_score > player_score:
            return "dealer"
        return "push"
    
    def resolve_round(self) -> str:
        """Resolve the current round and update chips."""
        winner = self.get_winner()
        
        if winner == "player":
            if self.player.hand.is_blackjack():
                self.player.chips += self.player.current_bet * 2.5  # 3:2 payout
            else:
                self.player.win_bet()
        elif winner == "dealer":
            self.player.lose_bet()
        else:
            self.player.push_bet()
        
        return winner
    
    def reset_round(self) -> None:
        """Reset hands for a new round."""
        self.player.reset_hand()
        self.dealer.reset_hand()
    
    def is_bankrupt(self) -> bool:
        """Check if player is bankrupt."""
        return self.player.chips <= 0
