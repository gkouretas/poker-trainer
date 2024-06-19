from ptypes import Card
from typing import Callable

class Player:
    def __init__(self, is_bot: bool) -> None:
        self.cards: tuple[Card] | None = None
        self.stack: int = 0
        self.ev: float = 0.0
        self.amount: float = 0.0
        
        self._is_bot = is_bot
        
    def __repr__(self) -> str:
        return f"Player. Hand: {self.cards}. Stack: {self.stack}"
        
    def request_chips(self, validity_callback: Callable[[int], bool]) -> int:
        while True:
            ret = input(f"Player: {hex(self.__hash__())}. Hand: {self.cards}. Stack/Bet: {self.stack}/{self.amount}. Action?: ")
            try:
                val = int(ret)
                if val != 0 and (val < self.amount or val > self.stack):
                    print(f"Invalid bet sizing: {val}. Must be greater than or equal to current amount and less than your current stack")
                elif validity_callback(val): 
                    return self.pay_amount(max(0, val - self.amount))
            except ValueError:
                print(f"Invalid action: {ret}. Must be number of chips")

    def pay_amount(self, request: float):
        val = min(request, self.stack)
        self.stack -= val
        self.amount += val
        return val
        
    def reset_amount(self, amount: float):
        self.stack += amount
        self.amount -= amount

    def compute_ev(self):
        pass