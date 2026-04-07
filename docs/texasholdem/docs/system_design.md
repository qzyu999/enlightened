# Texas Hold'em Poker - System Design

## Overview

This document describes the system design for a Texas Hold'em Poker game implementation.

## Core Components

### 1. Card System (`src/cards.py`)

**Responsibilities:**
- Represent playing cards with suit and rank
- Manage a standard 52-card deck
- Handle shuffling and dealing

**Key Classes:**
- `Suit`: Enum for Hearts, Diamonds, Clubs, Spades
- `Rank`: Enum for 2-Ace with comparison operators
- `Card`: Immutable card representation
- `Deck`: Manages card collection, shuffling, dealing

### 2. Player System (`src/player.py`)

**Responsibilities:**
- Track player state (chips, hand, position)
- Handle player actions (fold, call, raise, check)
- Validate action availability

**Key Classes:**
- `Player`: Player state and actions

### 3. Betting System (`src/betting.py`)

**Responsibilities:**
- Manage betting rounds
- Track current bet amounts
- Handle all-in scenarios
- Validate betting actions

**Key Classes:**
- `BettingAction`: Enum for player actions
- `BettingRound`: Manages a single betting round

### 4. Pot System (`src/pot.py`)

**Responsibilities:**
- Track main pot and side pots
- Handle chip distribution
- Manage all-in player eligibility

**Key Classes:**
- `Pot`: Pot management with side pot support

### 5. Hand Evaluator (`src/hand_evaluator.py`)

**Responsibilities:**
- Evaluate 5-card poker hands
- Compare hands for ranking
- Identify hand type and kickers

**Key Classes:**
- `HandResult`: Evaluation result with ranking
- `HandEvaluator`: Hand evaluation logic

### 6. Game Engine (`src/game.py`)

**Responsibilities:**
- Orchestrate game flow
- Manage game phases
- Coordinate between components
- Determine winners

**Key Classes:**
- `GamePhase`: Enum for game states
- `TexasHoldemGame`: Main game controller

## Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Player    │───▶│  GameController  │───▶│  GameEngine  │
│   Input     │    └─────────────┘    └─────────────┘
└─────────────┘                                    │
                                                   ▼
                    ┌─────────────────────────────────────┐
                    │           Sub-Systems               │
                    │  ┌─────────┬─────────┬──────────┐  │
                    │  │ Betting │   Pot   │ HandEval │  │
                    │  │ Manager │ Manager │  System  │  │
                    │  └─────────┴─────────┴──────────┘  │
                    └─────────────────────────────────────┘
                                                   │
                                                   ▼
                    ┌─────────────┐    ┌─────────────┐
                    │  GameEngine  │───▶│  GameController  │───▶│   Output    │
                    └─────────────┘    └─────────────┘    └─────────────┘
```

## Game Flow

1. **Setup Phase**
   - Players join the game
   - Blinds are posted
   
2. **Pre-Flop**
   - Each player receives 2 hole cards
   - First betting round
   
3. **Flop**
   - 3 community cards dealt
   - Second betting round
   
4. **Turn**
   - 4th community card dealt
   - Third betting round
   
5. **River**
   - 5th community card dealt
   - Fourth betting round
   
6. **Showdown**
   - Remaining players reveal hands
   - Best hand wins pot

## Design Decisions

### 1. Immutable Cards
Cards are immutable to prevent accidental modification and ensure thread safety.

### 2. Side Pot Support
The Pot class supports side pots for all-in scenarios, ensuring fair distribution.

### 3. Separation of Concerns
Each component has a single responsibility, making the system maintainable and testable.

### 4. Enum-Based Actions
Using enums for actions and phases provides type safety and clear state transitions.
