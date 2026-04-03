# System Architecture

## Overview

The Blackjack game follows a layered architecture with clear separation of concerns.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Console UI]
    end
    
    subgraph "Application Layer"
        Game[Game Controller]
    end
    
    subgraph "Domain Layer"
        Player[Player]
        Dealer[Dealer]
        Hand[Hand]
        Deck[Deck]
        Card[Card]
    end
    
    subgraph "Infrastructure"
        RNG[Random Number Generator]
    end
    
    UI --> Game
    Game --> Player
    Game --> Dealer
    Player --> Hand
    Dealer --> Hand
    Hand --> Card
    Deck --> Card
    Deck --> RNG
```

## Layer Descriptions

| Layer | Responsibility |
|-------|----------------|
| Presentation | Console input/output, user interaction |
| Application | Game flow control, rule enforcement |
| Domain | Core entities: Card, Deck, Hand, Player, Dealer |
| Infrastructure | Random number generation, utilities |
