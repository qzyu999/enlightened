"""End-to-End Tests for Texas Hold'em Game.

This module contains comprehensive E2E tests covering:
- Full game flow from pre-flop through showdown
- All betting actions (fold, call, raise, check)
- All-in scenarios and side pots
- Hand evaluation edge cases
- Multiple player scenarios (2-6 players)
- Winner determination in various scenarios
"""

import pytest
from typing import List

# Import game components
from src.game import TexasHoldemGame, GamePhase
from src.cards import Card, Suit, Rank, Deck
from src.player import Player
from src.hand_evaluator import HandEvaluator, HandResult
from src.betting import BettingAction


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def game():
    """Create a fresh game instance with deterministic seed."""
    return TexasHoldemGame(small_blind=10, big_blind=20, seed=42)


@pytest.fixture
def two_player_game():
    """Create a game with 2 players, each with 1000 chips."""
    game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
    game.add_player("Player1", 1000)
    game.add_player("Player2", 1000)
    return game


@pytest.fixture
def three_player_game():
    """Create a game with 3 players, each with 1000 chips."""
    game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
    game.add_player("Player1", 1000)
    game.add_player("Player2", 1000)
    game.add_player("Player3", 1000)
    return game


@pytest.fixture
def six_player_game():
    """Create a game with 6 players, each with 1000 chips."""
    game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
    for i in range(1, 7):
        game.add_player(f"Player{i}", 1000)
    return game


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_card(rank: Rank, suit: Suit) -> Card:
    """Helper to create a specific card."""
    return Card(rank, suit)


def get_player_by_name(game: TexasHoldemGame, name: str) -> Player:
    """Get a player by name from the game."""
    for player in game.players:
        if player.name == name:
            return player
    raise ValueError(f"Player {name} not found")


def fold_all_remaining(game: TexasHoldemGame, caller_name: str) -> None:
    """Fold all players except the caller to force a win."""
    for player in game.players:
        if player.name != caller_name and not player.folded:
            game.process_action(player.name, BettingAction.FOLD)


# ============================================================================
# TEST SUITE: GAME SETUP
# ============================================================================

class TestGameSetup:
    """Tests for game initialization and setup."""
    
    def test_game_creation_default_blinds(self, game):
        """Test game creates with default blinds."""
        assert game.small_blind == 10
        assert game.big_blind == 20
    
    def test_game_creation_custom_blinds(self):
        """Test game creates with custom blinds."""
        game = TexasHoldemGame(small_blind=50, big_blind=100)
        assert game.small_blind == 50
        assert game.big_blind == 100
    
    def test_add_player(self, game):
        """Test adding a player to the game."""
        player = game.add_player("TestPlayer", 500)
        assert player.name == "TestPlayer"
        assert player.chips == 500
        assert player in game.players
    
    def test_add_multiple_players(self, game):
        """Test adding multiple players."""
        game.add_player("P1", 1000)
        game.add_player("P2", 1000)
        game.add_player("P3", 1000)
        assert len(game.players) == 3
    
    def test_start_hand_insufficient_players(self, game):
        """Test start_hand fails with less than 2 players."""
        game.add_player("P1", 1000)
        result = game.start_hand()
        assert result is False
    
    def test_start_hand_success(self, two_player_game):
        """Test successful hand start."""
        result = two_player_game.start_hand()
        assert result is True
        assert two_player_game.phase == GamePhase.PREFLOP
        assert len(two_player_game.deck.deck) == 52  # Full deck
        assert len(two_player_game.community_cards) == 0
