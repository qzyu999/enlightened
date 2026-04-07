"""Entry point for running the Texas Hold'em game."""

from .game import TexasHoldemGame as Game


def main():
    """Main entry point for the game."""
    print("="*60)
    print("       Texas Hold'em Poker Game")
    print("="*60)
    print()
    
    # Create a new game with default settings
    game = Game()
    
    # Start the game loop
    game.run()


if __name__ == "__main__":
    main()
