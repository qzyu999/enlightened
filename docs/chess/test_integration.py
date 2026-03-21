from chess.engine.game import Game
from chess.ui.cli import ChessCLI
from chess.models.position import Position

def test_integration():
    game = Game()
    cli = ChessCLI()
    
    # Simulate a basic move: e2e4
    start_pos = Position(1, 4)
    end_pos = Position(3, 4)
    
    # Check move
    assert game.make_move(start_pos, end_pos) == True
    
    # Display board (captured in stdout)
    cli.display_board(game.board)
    
    # Check next turn
    assert game.turn.name == "BLACK"
    
    # Check if we can parse algebraic notation
    parsed = cli.parse_move("e7e5")
    assert parsed is not None
    assert parsed[0] == Position(6, 4)
    assert parsed[1] == Position(4, 4)
    
    print("Integration test passed!")

if __name__ == "__main__":
    test_integration()
