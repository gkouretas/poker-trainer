from ptypes import Card

class Player:
    def __init__(self) -> None:
        self.cards: tuple[Card] | None = None
        self._ev: float = 0.0
        
    def __repr__(self) -> str:
        return f"Player: {self.cards}"
        
    def compute_ev():
        pass