from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    row: int
    col: int

    @staticmethod
    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def __post_init__(self):
        if not self.is_valid(self.row, self.col):
            raise ValueError(f"Position ({self.row}, {self.col}) out of bounds (0-7).")

    def __repr__(self):
        return f"({self.row}, {self.col})"
