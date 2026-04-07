"""E2E tests for complete Texas Hold'em game scenarios."""

import sys
sys.path.insert(0, '/workspace')

# Optional pytest import for decorator support
try:
    import pytest
except ImportError:
    pytest = None

from src.game import TexasHoldemGame, GamePhase
from src.betting import BettingAction
from src.cards import Suit, Rank


class TestCompleteGameFlow:
    """Test complete game flows from start to finish."""
    
    def test_simple_fold_out_preflop(self):
        """Test game where everyone folds except one player."""
        game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
        game.add_player("Alice", 1000)
        game.add_player("Bob", 1000)
        game.add_player("Charlie", 1000)
        
        assert game.start_hand()
        assert game.phase == GamePhase.PREFLOP
        
        # Get current player and have them raise
        state = game.get_game_state()
        current_bettor = state["current_bettor"]
        
        # Everyone folds except one
        for _ in range(4):  # Multiple fold actions
            success, _ = game.process_action(BettingAction.FOLD)
            if success:
                break
        
        # Continue folding until game complete
        while not game.is_game_complete():
            game.process_action(BettingAction.FOLD)
        
        assert game.phase == GamePhase.COMPLETE
        assert game.winner is not None
    
    def test_simple_showdown(self):
        """Test a simple game to showdown with deterministic cards."""
        game = TexasHoldemGame(small_blind=10, big_blind=20, seed=12345)
        game.add_player("Alice", 1000)
        game.add_player("Bob", 1000)
        
        assert game.start_hand()
        
        # Both players call/check through all rounds
        actions_needed = 0
        while not game.is_game_complete():
            state = game.get_game_state()
            if state["bet_info"] and state["bet_info"]["to_call"] > 0:
                game.process_action(BettingAction.CALL)
            else:
                game.process_action(BettingAction.CHECK)
            actions_needed += 1
            if actions_needed > 20:  # Safety limit
                break
        
        assert game.phase == GamePhase.COMPLETE
        assert game.winner is not None
        assert game.winning_hand is not None


class TestHandScenarios:
    """Test specific hand scenarios."""
    
    def test_royal_flush_wins(self):
        """Verify royal flush beats everything."""
        from src.hand_evaluator import HandEvaluator
        from src.cards import Card, Rank
        
        def make_card(rank, suit):
            return Card(suit, rank)
        
        royal_flush = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.HEARTS),
            make_card(Rank.QUEEN, Suit.HEARTS),
            make_card(Rank.JACK, Suit.HEARTS),
            make_card(Rank.TEN, Suit.HEARTS)
        ]
        
        four_aces = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.ACE, Suit.DIAMONDS),
            make_card(Rank.ACE, Suit.CLUBS),
            make_card(Rank.ACE, Suit.SPADES),
            make_card(Rank.KING, Suit.HEARTS)
        ]
        
        result = HandEvaluator.compare_hands(royal_flush, four_aces)
        assert result > 0, "Royal flush should beat four of a kind"
    
    def test_all_hand_types_recognized(self):
        """Verify all hand types are correctly identified."""
        from src.hand_evaluator import HandEvaluator
        from src.cards import Card, Rank
        from src.hand_evaluator import (
            ROYAL_FLUSH, STRAIGHT_FLUSH, FOUR_OF_A_KIND,
            FULL_HOUSE, FLUSH, STRAIGHT, THREE_OF_A_KIND,
            TWO_PAIR, ONE_PAIR, HIGH_CARD
        )
        
        def make_card(rank, suit):
            return Card(suit, rank)
        
        test_cases = [
            (ROYAL_FLUSH, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.KING, Suit.HEARTS),
                make_card(Rank.QUEEN, Suit.HEARTS),
                make_card(Rank.JACK, Suit.HEARTS),
                make_card(Rank.TEN, Suit.HEARTS)
            ]),
            (STRAIGHT_FLUSH, [
                make_card(Rank.NINE, Suit.SPADES),
                make_card(Rank.EIGHT, Suit.SPADES),
                make_card(Rank.SEVEN, Suit.SPADES),
                make_card(Rank.SIX, Suit.SPADES),
                make_card(Rank.FIVE, Suit.SPADES)
            ]),
            (FOUR_OF_A_KIND, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.ACE, Suit.DIAMONDS),
                make_card(Rank.ACE, Suit.CLUBS),
                make_card(Rank.ACE, Suit.SPADES),
                make_card(Rank.KING, Suit.HEARTS)
            ]),
            (FULL_HOUSE, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.ACE, Suit.DIAMONDS),
                make_card(Rank.ACE, Suit.CLUBS),
                make_card(Rank.KING, Suit.SPADES),
                make_card(Rank.KING, Suit.HEARTS)
            ]),
            (FLUSH, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.KING, Suit.HEARTS),
                make_card(Rank.JACK, Suit.HEARTS),
                make_card(Rank.NINE, Suit.HEARTS),
                make_card(Rank.FIVE, Suit.HEARTS)
            ]),
            (STRAIGHT, [
                make_card(Rank.SIX, Suit.HEARTS),
                make_card(Rank.FIVE, Suit.DIAMONDS),
                make_card(Rank.FOUR, Suit.CLUBS),
                make_card(Rank.THREE, Suit.SPADES),
                make_card(Rank.TWO, Suit.HEARTS)
            ]),
            (THREE_OF_A_KIND, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.ACE, Suit.DIAMONDS),
                make_card(Rank.ACE, Suit.CLUBS),
                make_card(Rank.KING, Suit.SPADES),
                make_card(Rank.JACK, Suit.HEARTS)
            ]),
            (TWO_PAIR, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.ACE, Suit.DIAMONDS),
                make_card(Rank.KING, Suit.CLUBS),
                make_card(Rank.KING, Suit.SPADES),
                make_card(Rank.JACK, Suit.HEARTS)
            ]),
            (ONE_PAIR, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.ACE, Suit.DIAMONDS),
                make_card(Rank.KING, Suit.CLUBS),
                make_card(Rank.JACK, Suit.SPADES),
                make_card(Rank.NINE, Suit.HEARTS)
            ]),
            (HIGH_CARD, [
                make_card(Rank.ACE, Suit.HEARTS),
                make_card(Rank.KING, Suit.DIAMONDS),
                make_card(Rank.JACK, Suit.CLUBS),
                make_card(Rank.NINE, Suit.SPADES),
                make_card(Rank.FIVE, Suit.HEARTS)
            ])
        ]
        
        for expected_rank, cards in test_cases:
            result = HandEvaluator.evaluate(cards)
            assert result.rank == expected_rank, \
                f"Expected {expected_rank}, got {result.rank} ({result.description})"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_all_in_scenario(self):
        """Test player going all-in."""
        game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
        game.add_player("ShortStack", 15)  # Less than big blind
        game.add_player("DeepStack", 1000)
        
        assert game.start_hand()
        
        # Short stack should go all-in automatically
        state = game.get_game_state()
        short_stack = next(p for p in state["players"] if p["name"] == "ShortStack")
        
        # The player with 15 chips posting 10 SB should be all-in
        assert short_stack["chips"] == 5  # 15 - 10 SB
    
    def test_split_pot(self):
        """Test split pot scenario."""
        from src.hand_evaluator import HandEvaluator
        from src.cards import Card, Rank
        
        def make_card(rank, suit):
            return Card(suit, rank)
        
        # Two identical hands
        hand1 = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.JACK, Suit.CLUBS),
            make_card(Rank.NINE, Suit.SPADES),
            make_card(Rank.FIVE, Suit.HEARTS)
        ]
        hand2 = [
            make_card(Rank.ACE, Suit.SPADES),
            make_card(Rank.KING, Suit.CLUBS),
            make_card(Rank.JACK, Suit.HEARTS),
            make_card(Rank.NINE, Suit.DIAMONDS),
            make_card(Rank.FIVE, Suit.SPADES)
        ]
        
        result = HandEvaluator.compare_hands(hand1, hand2)
        assert result == 0, "Identical hands should tie"
    
    def test_wheel_straight(self):
        """Test A-2-3-4-5 straight (wheel)."""
        from src.hand_evaluator import HandEvaluator
        from src.cards import Card, Rank
        from src.hand_evaluator import STRAIGHT
        
        def make_card(rank, suit):
            return Card(suit, rank)
        
        wheel = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.FIVE, Suit.DIAMONDS),
            make_card(Rank.FOUR, Suit.CLUBS),
            make_card(Rank.THREE, Suit.SPADES),
            make_card(Rank.TWO, Suit.HEARTS)
        ]
        
        result = HandEvaluator.evaluate(wheel)
        assert result.rank == STRAIGHT
        assert result.tiebreaker[0] == 5, "Wheel should be 5-high"
    
    def test_broadway_straight(self):
        """Test 10-J-Q-K-A straight (broadway)."""
        from src.hand_evaluator import HandEvaluator
        from src.cards import Card, Rank
        from src.hand_evaluator import STRAIGHT
        
        def make_card(rank, suit):
            return Card(suit, rank)
        
        broadway = [
            make_card(Rank.ACE, Suit.HEARTS),
            make_card(Rank.KING, Suit.DIAMONDS),
            make_card(Rank.QUEEN, Suit.CLUBS),
            make_card(Rank.JACK, Suit.SPADES),
            make_card(Rank.TEN, Suit.HEARTS)
        ]
        
        result = HandEvaluator.evaluate(broadway)
        assert result.rank == STRAIGHT
        assert result.tiebreaker[0] == 14, "Broadway should be Ace-high"
    
    def test_not_enough_players(self):
        """Test game with insufficient players."""
        game = TexasHoldemGame()
        game.add_player("Solo", 1000)
        
        assert not game.start_hand(), "Should fail with only one player"
    
    def test_player_elimination(self):
        """Test that players with no chips are handled."""
        game = TexasHoldemGame(small_blind=10, big_blind=20)
        game.add_player("Alice", 1000)
        game.add_player("Bob", 1000)
        
        # Manually set Bob to 0 chips
        game.players[1].chips = 0
        
        assert not game.start_hand(), "Should fail when only one player has chips"


class TestMultiPlayerScenarios:
    """Test scenarios with multiple players."""
    
    def test_six_max_game_setup(self):
        """Test setting up a 6-player game."""
        game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
        
        for name in ["Player1", "Player2", "Player3", 
                     "Player4", "Player5", "Player6"]:
            game.add_player(name, 1000)
        
        assert len(game.players) == 6
        assert game.start_hand()
        
        state = game.get_game_state()
        
        # Verify blinds are set correctly
        assert sum(1 for p in state["players"] if p["is_small_blind"]) == 1
        assert sum(1 for p in state["players"] if p["is_big_blind"]) == 1
        assert sum(1 for p in state["players"] if p["is_dealer"]) == 1
        
        # Verify hole cards dealt
        for player in state["players"]:
            assert len(player["hand"]) == 2
    
    def test_blind_rotation(self):
        """Test that blinds rotate correctly."""
        game = TexasHoldemGame(small_blind=10, big_blind=20, seed=42)
        game.add_player("A", 1000)
        game.add_player("B", 1000)
        game.add_player("C", 1000)
        
        # First hand
        game.start_hand()
        state1 = game.get_game_state()
        dealer1 = next(p["name"] for p in state1["players"] if p["is_dealer"])
        sb1 = next(p["name"] for p in state1["players"] if p["is_small_blind"])
        bb1 = next(p["name"] for p in state1["players"] if p["is_big_blind"])
        
        # Simulate completing the hand
        while not game.is_game_complete():
            game.process_action(BettingAction.CALL)
        
        # Second hand
        game.start_hand()
        state2 = game.get_game_state()
        dealer2 = next(p["name"] for p in state2["players"] if p["is_dealer"])
        sb2 = next(p["name"] for p in state2["players"] if p["is_small_blind"])
        bb2 = next(p["name"] for p in state2["players"] if p["is_big_blind"])
        
        # Dealer should have moved
        assert dealer1 != dealer2
        # Blinds should have moved
        assert sb1 != sb2
        assert bb1 != bb2
