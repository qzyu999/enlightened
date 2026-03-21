from enum import Enum, auto

class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def opponent(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE
