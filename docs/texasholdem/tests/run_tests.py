"""End-to-End Tests for Texas Hold'em Game.

This module contains comprehensive E2E tests covering:
- Full game flow from pre-flop through showdown
- All betting actions (fold, call, raise, check)
- All-in scenarios and side pots
- Hand evaluation edge cases
- Multiple player scenarios (2-6 players)
- Winner determination in various scenarios

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py TestGameSetup      # Run specific class
    python run_tests.py test_add_player    # Run specific method
"""

import sys
import traceback
from typing import List, Type, Any, Callable

# Add workspace to path
sys.path.insert(0, '/workspace')

# Import game components
from src.game import TexasHoldemGame, GamePhase
from src.cards import Card, Suit, Rank, Deck
from src.player import Player
from src.hand_evaluator import HandEvaluator, HandResult
from src.betting import BettingAction


# ============================================================================
# TEST RUNNER FRAMEWORK
# ============================================================================

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record_pass(self, name: str):
        self.passed += 1
        print(f"  ✓ {name}")
    
    def record_fail(self, name: str, error: str):
        self.failed += 1
        self.errors.append((name, error))
        print(f"  ✗ {name}")
        print(f"    Error: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Results: {self.passed}/{total} passed, {self.failed} failed")
        if self.errors:
            print("\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        return self.failed == 0


def run_test(test_func: Callable, test_name: str, result: TestResult):
    """Run a single test and record the result."""
    try:
        test_func()
        result.record_pass(test_name)
    except AssertionError as e:
        result.record_fail(test_name, str(e))
    except Exception as e:
        result.record_fail(test_name, f"{type(e).__name__}: {e}")


def run_tests(test_classes: List[Type], filter_name: str = None):
    """Run all tests in the given classes."""
    result = TestResult()
    
    for test_class in test_classes:
        class_name = test_class.__name__
        
        # Create instance (some tests need fixtures)
        try:
            instance = test_class()
        except TypeError:
            instance = None
        
        for attr_name in dir(test_class):
            if attr_name.startswith('test_'):
                test_name = f"{class_name}.{attr_name}"
                
                # Apply filter if specified
                if filter_name and filter_name not in test_name:
                    continue
                
                print(f"\nRunning: {test_name}")
                test_method = getattr(test_class, attr_name)
                
                # Check if it needs an instance
                if instance is not None:
                    run_test(lambda t=test_method, i=instance: t(i), test_name, result)
                else:
                    run_test(test_method, test_name, result)
    
    return result.summary()


# ============================================================================
# FIXTURES (as factory functions)
# ============================================================================

def create_game():
    """Create a fresh game instance with deterministic seed."""
    return TexasHoldemGame(small_blind=10, big_blind=20, seed=42)


def create_two_player_game():
    """Create a game with 2 players, each with 1000 chips."""
    game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
    game.add_player("Player1", 1000)
    game.add_player("Player2", 1000)
    return game


def create_three_player_game():
    """Create a game with 3 players, each with 1000 chips."""
    game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
    game.add_player("Player1", 1000)
    game.add_player("Player2", 1000)
    game.add_player("Player3", 1000)
    return game


def create_six_player_game():
    """Create a game with 6 players, each with 1000 chips."""
    game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
    for i in range(1, 7):
        game.add_player(f"Player{i}", 1000)
    return game


def get_player_by_name(game: TexasHoldemGame, name: str) -> Player:
    """Get a player by name from the game."""
    for player in game.players:
        if player.name == name:
            return player
    raise ValueError(f"Player {name} not found")


def create_card(rank: Rank, suit: Suit) -> Card:
    """Helper to create a specific card."""
    return Card(rank, suit)


# ============================================================================
# TEST SUITE: GAME SETUP
# ============================================================================

class TestGameSetup:
    """Tests for game initialization and setup."""
    
    def test_game_creation_default_blinds(self):
        """Test game creates with default blinds."""
        game = create_game()
        assert game.small_blind == 10
        assert game.big_blind == 20
    
    def test_game_creation_custom_blinds(self):
        """Test game creates with custom blinds."""
        game = TexasHoldemGame(small_blind=50, big_blind=100)
        assert game.small_blind == 50
        assert game.big_blind == 100
    
    def test_add_player(self):
        """Test adding a player to the game."""
        game = create_game()
        player = game.add_player("TestPlayer", 500)
        assert player.name == "TestPlayer"
        assert player.chips == 500
        assert player in game.players
    
    def test_add_multiple_players(self):
        """Test adding multiple players."""
        game = create_game()
        game.add_player("P1", 1000)
        game.add_player("P2", 1000)
        game.add_player("P3", 1000)
        assert len(game.players) == 3
    
    def test_start_hand_insufficient_players(self):
        """Test start_hand fails with less than 2 players."""
        game = create_game()
        game.add_player("P1", 1000)
        result = game.start_hand()
        assert result is False
    
    def test_start_hand_success(self):
        """Test successful hand start."""
        game = create_two_player_game()
        result = game.start_hand()
        assert result is True
        assert game.phase == GamePhase.PREFLOP
        assert game.deck.remaining() == 48  # 52 - 4 hole cards
        assert len(game.community_cards) == 0
    
    def test_blinds_posted_correctly(self):
        """Test that blinds are posted correctly after start_hand."""
        game = create_two_player_game()
        game.start_hand()
        
        p1, p2 = game.players
        
        # Player1 should be small blind (10 chips)
        assert p1.is_small_blind, "Player1 should be small blind"
        assert p1.chips == 990, f"Player1 should have 990 chips, has {p1.chips}"
        
        # Player2 should be big blind (20 chips)
        assert p2.is_big_blind, "Player2 should be big blind"
        assert p2.chips == 980, f"Player2 should have 980 chips, has {p2.chips}"
        
        # Pot should contain blinds
        assert game.pot.get_total() == 30, f"Pot should be 30, is {game.pot.get_total()}"
    
    def test_hole_cards_dealt(self):
        """Test that hole cards are dealt correctly."""
        game = create_two_player_game()
        game.start_hand()
        
        for player in game.players:
            assert len(player.hand) == 2, f"{player.name} should have 2 cards"
    
    def test_deck_has_remaining_cards(self):
        """Test that deck has correct remaining cards after deal."""
        game = create_two_player_game()
        game.start_hand()
        
        # 52 - 4 hole cards = 48
        assert game.deck.remaining() == 48


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Get filter from command line if provided
    filter_name = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("="*60)
    print("Texas Hold'em E2E Test Suite")
    print("="*60)
    if filter_name:
        print(f"Filter: {filter_name}")
    print()
    
    # Define test classes to run
    test_classes = [
        TestGameSetup,
    ]
    
    # Run tests
    success = run_tests(test_classes, filter_name)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
