# Texas Hold'em Poker Game

A command-line Texas Hold'em poker game implementation.

## Game Overview

This is a Texas Hold'em poker game that supports multiple players with the following features:

- **Player Support**: 2-6 players (standard poker table size)
- **Blind System**: Configurable small and big blinds
- **Complete Betting Rounds**: Pre-flop, flop, turn, and river
- **Hand Evaluation**: Full poker hand ranking from High Card to Royal Flush
- **Side Pots**: Proper handling of all-in scenarios
- **Dealer Button Rotation**: Automatic dealer position rotation

## Quick Start

```bash
# Run the game
python -m src.game
```

## Game Rules

### Basic Rules

1. **Ante/Blinds**: Before each hand, players post blinds (small blind and big blind)
2. **Hole Cards**: Each player receives 2 private cards
3. **Betting Rounds**: Four rounds of betting occur:
   - **Pre-flop**: After hole cards are dealt
   - **Flop**: After 3 community cards are dealt
   - **Turn**: After 4th community card is dealt
   - **River**: After 5th community card is dealt
4. **Showdown**: Remaining players reveal hands; best hand wins

### Betting Actions

| Action | Description |
|--------|-------------|
| **Fold** | Surrender hand and exit the current hand |
| **Check** | Pass action to next player without betting (only if no bet exists) |
| **Call** | Match the current bet |
| **Raise** | Increase the current bet |

### Hand Rankings (Best to Worst)

1. **Royal Flush** - A, K, Q, J, 10, all same suit
2. **Straight Flush** - Five consecutive cards, same suit
3. **Four of a Kind** - Four cards of same rank
4. **Full House** - Three of a kind + a pair
5. **Flush** - Five cards of same suit
6. **Straight** - Five consecutive cards
7. **Three of a Kind** - Three cards of same rank
8. **Two Pair** - Two different pairs
9. **One Pair** - Two cards of same rank
10. **High Card** - Highest card when no other hand

## How to Play

### Starting a Game

1. Create a game with 2-6 players
2. Set blind amounts (optional, defaults to 10/20)
3. Start playing hands

### During a Hand

1. **Pre-flop**: You receive 2 hole cards
2. **Betting**: Choose your action (fold, check, call, raise)
3. **Community Cards**: 5 cards dealt face-up over 3 streets
4. **Showdown**: Best 5-card hand wins the pot

### Special Situations

- **All-in**: If you bet all your chips, you're all-in and can only win pots you contributed to
- **Side Pots**: Created when a player goes all-in; other players continue betting
- **Split Pot**: If hands tie, the pot is split equally

## Hand Rankings Details

### Royal Flush
The highest possible hand. A, K, Q, J, 10 all of the same suit.

**Example**: A♠ K♠ Q♠ J♠ 10♠

### Straight Flush
Five consecutive cards of the same suit (not A-K-Q-J-10).

**Example**: 8♥ 7♥ 6♥ 5♥ 4♥

### Four of a Kind
Four cards of the same rank plus any fifth card.

**Example**: Q♣ Q♦ Q♥ Q♠ 7♣

### Full House
Three cards of one rank plus two cards of another rank.

**Example**: K♣ K♦ K♥ 5♠ 5♣

### Flush
Five cards of the same suit, not in sequence.

**Example**: A♣ 9♣ 7♣ 4♣ 2♣

### Straight
Five consecutive cards of mixed suits.

**Example**: 9♠ 8♥ 7♦ 6♣ 5♠

**Note**: Aces can be high (A-K-Q-J-10) or low (A-2-3-4-5, called a "wheel").

### Three of a Kind
Three cards of the same rank plus two unrelated cards.

**Example**: 7♣ 7♦ 7♥ K♠ 3♣

### Two Pair
Two cards of one rank, two cards of another rank, plus one unrelated card.

**Example**: A♣ A♦ 8♠ 8♥ 4♣

### One Pair
Two cards of the same rank plus three unrelated cards.

**Example**: J♣ J♦ K♠ 9♥ 3♣

### High Card
When no other hand is made, the highest card wins.

**Example**: A♣ K♦ 9♠ 5♥ 2♣

## Betting Examples

### Example 1: Simple Hand
```
Players: Alice ($1000), Bob ($1000)
Blinds: 10/20

Pre-flop:
- Bob posts big blind $20
- Alice posts small blind $10
- Alice raises to $40
- Bob calls $40

Flop: K♠ 7♥ 2♦
- Alice checks
- Bob bets $50
- Alice calls $50

Turn: Q♣
- Both check

River: 9♠
- Alice bets $100
- Bob folds

Result: Alice wins the pot!
```

### Example 2: All-in Scenario
```
Players: Alice ($50), Bob ($500)
Blinds: 10/20

Pre-flop:
- Bob posts big blind $20
- Alice posts small blind $10
- Alice raises all-in $50
- Bob calls $50

Result: Main pot $100, side pot $400 (Bob only)
```

## FAQ

**Q: How many players can play?**
A: 2-6 players (standard poker table size).

**Q: What happens if a player runs out of chips?**
A: The player is eliminated from the game.

**Q: Can I raise any amount?**
A: Raises must be at least the minimum raise amount (typically equal to the big blind).

**Q: How are ties handled?**
A: The pot is split equally among tied players.

**Q: What is the minimum stack to play?**
A: You need at least enough chips to cover the big blind.

---

*For technical details, see the source code in `/src/`*

