from enum import Enum, auto


class ProgramState(Enum):
    """Every screen the program can show."""
    MainMenu = auto()
    Application = auto()   # the "Modes" menu
    Normal = auto()
    Movement = auto()
    Highscore = auto()
