"""Simple manual test runner - no pytest required."""
import sys
sys.path.insert(0, '/workspace')

from src.cards import Card, Suit, Rank, Deck
from src.hand_evaluator import HandEvaluator, ONE_PAIR, FLUSH
from src.player import Player
from src.game import TexasHoldemGame, GamePhase
from src.betting import BettingAction

def test_deck():
    """Test deck creation and dealing."""
    deck = Deck()
    assert deck.remaining() == 52, "Deck should have 52 cards"
    card = deck.deal_one()
    assert deck.remaining() == 51, "Deck should have 51 cards after dealing one"
    print("✓ Deck tests passed")

def test_hand_evaluator():
    """Test hand evaluation."""
    evaluator = HandEvaluator()
    
    # Test pair (need 5 cards minimum) - Card(suit, rank)
    cards = [
        Card(Suit.HEARTS, Rank.TWO),
        Card(Suit.CLUBS, Rank.TWO),
        Card(Suit.DIAMONDS, Rank.FIVE),
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.HEARTS, Rank.NINE)
    ]
    result = evaluator.evaluate(cards)
    assert result.rank == ONE_PAIR, f"Expected ONE_PAIR, got {result.rank}"
    
    # Test flush
    flush_cards = [
        Card(Suit.HEARTS, Rank.TWO),
        Card(Suit.HEARTS, Rank.FIVE),
        Card(Suit.HEARTS, Rank.SEVEN),
        Card(Suit.HEARTS, Rank.JACK),
        Card(Suit.HEARTS, Rank.KING)
    ]
    result = evaluator.evaluate(flush_cards)
    assert result.rank == FLUSH, f"Expected FLUSH, got {result.rank}"
    
    print("✓ Hand evaluator tests passed")

def test_player():
    """Test player functionality."""
    player = Player("TestPlayer", 1000)
    assert player.chips == 1000
    player.call(100)
    assert player.chips == 900
    print("✓ Player tests passed")

def test_basic_game():
    """Test a basic game flow."""
    game = TexasHoldemGame()
    game.add_player("Alice", 1000)
    game.add_player("Bob", 1000)
    
    game.start_hand()
    print(f"Phase after start_hand: {game.phase}")
    assert game.phase == GamePhase.PREFLOP, f"Expected PREFLOP, got {game.phase}"
    
    # Alice is big blind (dealer), Bob is small blind
    # Bob acts first (UTG), he folds
    success, msg = game.process_action(BettingAction.FOLD)
    print(f"Bob folds: {success}, {msg}")
    
    # Game should be complete with Alice as winner
    print(f"Phase after Bob folds: {game.phase}")
    print(f"Is game complete: {game.is_game_complete()}")
    
    assert game.is_game_complete(), "Game should be complete after Bob folds"
    
    winner_info = game.get_winner_info()
    print(f"Winner info: {winner_info}")
    assert winner_info is not None, "Should have winner info"
    assert winner_info['winner'] == "Alice", f"Expected Alice to win, got {winner_info['winner']}"
    print("✓ Basic game test passed")

def main():
    print("\n=== Running Manual Tests ===")
    try:
        test_deck()
        test_hand_evaluator()
        test_player()
        test_basic_game()
        print("\n=== ALL TESTS PASSED ===")
        return 0
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
