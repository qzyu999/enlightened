"""UI module for Blackjack game."""
from src.game_engine import GameEngine
from src.entities import Player, Dealer


class BlackjackUI:
    """Command-line interface for Blackjack."""
    
    def __init__(self):
        self.engine = GameEngine()
    
    def display_hand(self, hand, hidden_first: bool = False) -> None:
        """Display a hand, optionally hiding first card."""
        if hidden_first and len(hand.cards) > 1:
            cards = ["[Hidden]"] + [str(c) for c in hand.cards[1:]]
            print(f"  Hand: {', '.join(cards)}")
        else:
            print(f"  Hand: {', '.join(str(c) for c in hand.cards)}")
            print(f"  Score: {hand.get_score()}")
    
    def display_status(self, show_dealer_full: bool = False) -> None:
        """Display current game status."""
        print("\n" + "="*40)
        print(f"Player: ${self.engine.player.chips} | Bet: ${self.engine.player.current_bet}")
        print("="*40)
        print("\n👤 PLAYER:")
        self.display_hand(self.engine.player.hand)
        print("\n🎰 DEALER:")
        self.display_hand(self.engine.dealer.hand, hidden_first=not show_dealer_full)
        print()
    
    def get_bet(self) -> int:
        """Get valid bet from player."""
        while True:
            try:
                bet = int(input(f"\nPlace your bet (1-${self.engine.player.chips}): "))
                if 1 <= bet <= self.engine.player.chips:
                    return bet
                print(f"Invalid bet. Please enter 1-${self.engine.player.chips}")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_action(self) -> str:
        """Get player action (hit/stand)."""
        while True:
            action = input("\nHit (h) or Stand (s)? ").lower()
            if action in ('h', 'hit'):
                return 'hit'
            if action in ('s', 'stand'):
                return 'stand'
            print("Please enter 'h' for Hit or 's' for Stand.")
    
    def announce_result(self, winner: str) -> None:
        """Announce round result."""
        print("\n" + "="*40)
        if winner == "player":
            if self.engine.player.hand.is_blackjack():
                print("🎉 BLACKJACK! You win 3:2!")
            else:
                print("🎉 You win!")
        elif winner == "dealer":
            print("😞 Dealer wins!")
        else:
            print("🤝 Push! Bet returned.")
        print(f"Player chips: ${self.engine.player.chips}")
        print("="*40)
    
    def play_round(self) -> bool:
        """Play a single round. Returns True if game continues."""
        # Place bet
        bet = self.get_bet()
        self.engine.player.place_bet(bet)
        
        # Deal cards
        self.engine.deal_initial_cards()
        self.display_status()
        
        # Check for natural blackjack
        if self.engine.player.hand.is_blackjack():
            print("🎉 NATURAL BLACKJACK!")
            winner = self.engine.resolve_round()
            self.announce_result(winner)
            return not self.engine.is_bankrupt()
        
        # Player's turn
        while True:
            action = self.get_action()
            if action == 'hit':
                self.engine.player_hit()
                self.display_status()
                if self.engine.player.hand.is_bust():
                    print("💥 BUST! You went over 21!")
                    self.engine.resolve_round()
                    self.announce_result("dealer")
                    return not self.engine.is_bankrupt()
            else:
                self.engine.player_stand()
                break
        
        # Reveal dealer and resolve
        self.display_status(show_dealer_full=True)
        winner = self.engine.resolve_round()
        self.announce_result(winner)
        
        return not self.engine.is_bankrupt()
    
    def play_game(self) -> None:
        """Main game loop."""
        print("\n" + "="*40)
        print("🎰   WELCOME TO BLACKJACK   🎰")
        print("="*40)
        
        name = input("\nEnter your name: ").strip() or "Player"
        self.engine.setup(name)
        
        while True:
            self.engine.reset_round()
            if not self.play_round():
                print("\n💸 You're bankrupt! Game Over!")
                break
            
            if not input("\nPlay another round? (y/n): ").lower().startswith('y'):
                print(f"\nThanks for playing! You finished with ${self.engine.player.chips}!")
                break
