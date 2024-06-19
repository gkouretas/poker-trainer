from dataclasses import dataclass
from enum import Enum, IntEnum

class Suit(Enum):
    """Card suit"""
    SPADE = 0
    HEART = 1
    DIAMOND = 2
    CLUB = 3
    
    def char(self) -> str:
        if self.name == self.SPADE.name: return "♠"
        elif self.name == self.HEART.name: return "♥"
        elif self.name == self.DIAMOND.name: return "♦"
        elif self.name == self.CLUB.name: return "♣"
        else: return self.name
        
    
    def __repr__(self) -> str:
        return self.char()

class Rank(IntEnum):
    """Card rank"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    def __repr__(self) -> str:
        return f"{self if self <= 10 else self.name[0]}"

@dataclass(frozen = True)
class Card:
    """Dataclass containing card information"""
    rank: Rank
    suit: Suit
    
    def __repr__(self) -> str:
        return f"{self.rank.__repr__()}{self.suit.__repr__()}"
    
@dataclass
class Blinds:
    small: float
    big: float
    
    def total(self): return self.small + self.big
    
class Action(IntEnum):
    NULL = 0
    FOLD = 1
    CHECK = 2
    CALL = 3
    RAISE = 4