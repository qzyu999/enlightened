"""Main entry point for Blackjack game."""
from src.ui import BlackjackUI


def main():
    """Start the Blackjack game."""
    ui = BlackjackUI()
    ui.play_game()


if __name__ == "__main__":
    main()
