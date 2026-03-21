# Chess Game Design Architecture

## Project Overview
The goal is to build a modular, testable chess game engine in Python. The system is split into data representation (Models), rule-enforcement (Logic), and user interaction (UI).

## Core Components

### 1. Data Models (`chess/models/`)
*   **Color (Enum):** WHITE, BLACK.
*   **Position (Dataclass):** Represents coordinates (row, col) from (0, 0) to (7, 7).
*   **Piece (ABC):** Base class for all pieces.
    *   Attributes: `color: Color`, `position: Position`, `has_moved: bool`.
    *   Method: `get_valid_moves(board: Board) -> List[Position]`.
*   **Board:** Holds an 8x8 grid of `Piece` or `None`.
    *   Responsibilities: Retrieving/setting pieces, basic boundary checks.

### 2. Piece Logic (`chess/pieces/`)
Each piece (Pawn, Rook, Knight, Bishop, Queen, King) inherits from `Piece` and implements its own `get_valid_moves` logic.

### 3. Game Engine (`chess/engine.py`)
*   **Game:** Manages the state of the game.
    *   Current turn (WHITE/BLACK).
    *   Move history.
    *   Rule enforcement (Check, Checkmate, Stalemate, Castling, En Passant).
    *   Executing moves (updating piece positions on the board).

### 4. Interface (`chess/ui/`)
*   **CLI:** Initial implementation for displaying the board and taking user input (e.g., "e2e4").

## Directory Structure
```
chess/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── color.py
│   ├── position.py
│   ├── piece.py
│   └── board.py
├── pieces/
│   ├── __init__.py
│   ├── pawn.py
│   ├── rook.py
│   ├── knight.py
│   ├── bishop.py
│   ├── queen.py
│   └── king.py
├── engine/
│   ├── __init__.py
│   └── game.py
└── ui/
    ├── __init__.py
    └── cli.py
```
