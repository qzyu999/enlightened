# Texas Hold'em Poker Game - Architecture & System Design

## System Overview

A command-line Texas Hold'em poker game supporting multiple players with full game mechanics including betting rounds, hand evaluation, and pot management.

---

## Architectural Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        CLI[CLI Interface]
    end
    
    subgraph "Application Layer"
        GameEngine[Game Engine]
        GameLoop[Game Loop Controller]
    end
    
    subgraph "Domain Layer"
        Player[Player Manager]
        HandEval[Hand Evaluator]
        DeckMgr[Deck Manager]
        PotMgr[Pot Manager]
        BetMgr[Betting Manager]
    end
    
    subgraph "Infrastructure Layer"
        RNG[Random Number Generator]
        Logger[Logger]
    end
    
    CLI --> GameEngine
    GameEngine --> GameLoop
    GameLoop --> Player
    GameLoop --> HandEval
    GameLoop --> DeckMgr
    GameLoop --> PotMgr
    GameLoop --> BetMgr
    DeckMgr --> RNG
    Player --> BetMgr
    HandEval --> Player
```

---

## Component Architecture

```mermaid
classDiagram
    class GameEngine {
        +start_game()
        +next_round()
        +evaluate_hands()
        +determine_winner()
    }
    
    class Player {
        +name: str
        +chips: int
        +hand: List[Card]
        +folded: bool
        +call()
        +raise(amount)
        +fold()
        +check()
    }
    
    class Card {
        +suit: Suit
        +rank: Rank
        +value: int
    }
    
    class Deck {
        +cards: List[Card]
        +shuffle()
        +deal(count)
    }
    
    class HandEvaluator {
        +evaluate(cards)
        +get_hand_rank()
        +get_tiebreaker()
    }
    
    class Pot {
        +main_pot: int
        +side_pots: List[int]
        +add_chips(player, amount)
        +distribute(winner)
    }
    
    class BettingRound {
        +current_bet: int
        +active_players: List[Player]
        +next_player_index: int
        +process_action(player, action)
    }
    
    GameEngine --> Player
    GameEngine --> Deck
    GameEngine --> HandEvaluator
    GameEngine --> Pot
    GameEngine --> BettingRound
    Player --> Card
    Deck --> Card
    HandEvaluator --> Card
```

---

## Game Flow State Machine

```mermaid
stateDiagram-v2
    [*] --> PreFlop
    PreFlop --> Flop: All players act
    Flop --> Turn: All players act
    Turn --> River: All players act
    River --> Showdown: All players act
    Showdown --> [*]: Winner determined
    
    PreFlop --> FoldOut: All but one fold
    Flop --> FoldOut: All but one fold
    Turn --> FoldOut: All but one fold
    River --> FoldOut: All but one fold
    FoldOut --> [*]: Winner determined
```

---

## Hand Ranking System

```mermaid
graph LR
    A[Royal Flush] --> B[Straight Flush]
    B --> C[Four of a Kind]
    C --> D[Full House]
    D --> E[Flush]
    E --> F[Straight]
    F --> G[Three of a Kind]
    G --> H[Two Pair]
    H --> I[One Pair]
    I --> J[High Card]
```

### Hand Values (for comparison)
| Rank | Value | Description |
|------|-------|-------------|
| Royal Flush | 900 | A-K-Q-J-10, same suit |
| Straight Flush | 800 | 5 consecutive, same suit |
| Four of a Kind | 700 | 4 cards same rank |
| Full House | 600 | 3 of a kind + pair |
| Flush | 500 | 5 cards same suit |
| Straight | 400 | 5 consecutive cards |
| Three of a Kind | 300 | 3 cards same rank |
| Two Pair | 200 | 2 pairs |
| One Pair | 100 | 1 pair |
| High Card | 0 | No combination |

---

## Data Models

### Card
```python
Card {
    suit: Suit (Hearts, Diamonds, Clubs, Spades)
    rank: Rank (2-10, J, Q, K, A)
    value: int (2-14, where A=14)
}
```

### Player
```python
Player {
    id: str
    name: str
    chips: int
    hand: List[Card] (2 cards)
    folded: bool
    current_bet: int
    is_dealer: bool
    is_big_blind: bool
    is_small_blind: bool
}
```

### Game State
```python
GameState {
    players: List[Player]
    community_cards: List[Card] (0-5 cards)
    deck: Deck
    pot: Pot
    current_round: Round (PreFlop, Flop, Turn, River, Showdown)
    current_bettor: Player
    current_bet_amount: int
    min_bet: int
    max_bet: int
}
```

---

## Testing Architecture

```mermaid
graph TB
    subgraph "Unit Tests"
        UT1[Test Card Operations]
        UT2[Test Deck Shuffling]
        UT3[Test Hand Evaluation]
        UT4[Test Player Actions]
    end
    
    subgraph "Integration Tests"
        IT1[Test Betting Round]
        IT2[Test Pot Management]
        IT3[Test Round Transitions]
    end
    
    subgraph "E2E Tests"
        E2E1[Test Complete Game]
        E2E2[Test All Hand Types]
        E2E3[Test Edge Cases]
        E2E4[Test Multi-Player Scenarios]
    end
    
    UT1 --> IT1
    UT2 --> IT1
    UT3 --> IT2
    UT4 --> IT3
    IT1 --> E2E1
    IT2 --> E2E1
    IT3 --> E2E1
```

---

## File Structure

```
texas_holdem/
├── src/
│   ├── __init__.py
│   ├── cards.py          # Card, Suit, Rank, Deck classes
│   ├── player.py         # Player class and actions
│   ├── hand_evaluator.py # Hand ranking and evaluation
│   ├── pot.py            # Pot and side pot management
│   ├── betting.py        # Betting round management
│   ├── game.py           # Main game engine
│   └── cli.py            # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_cards.py
│   ├── test_hand_evaluator.py
│   ├── test_player.py
│   ├── test_pot.py
│   ├── test_betting.py
│   ├── test_game.py
│   └── e2e/
│       ├── __init__.py
│       ├── test_complete_games.py
│       ├── test_hand_scenarios.py
│       └── test_edge_cases.py
├── ARCHITECTURE.md
├── README.md
├── requirements.txt
└── pytest.ini
```

---

## Key Design Decisions

1. **Deterministic RNG for Testing**: The deck uses a configurable random seed, enabling reproducible test scenarios.

2. **Side Pot Support**: Full implementation of side pots for all-in scenarios.

3. **Position-Based Blinds**: Small blind and big blind rotate each hand.

4. **Hand Evaluation Efficiency**: Uses pre-computed rank values for O(1) hand comparisons.

5. **Action Validation**: All player actions are validated against game state before execution.

6. **Clean Separation**: Strict separation between game logic and CLI presentation.
