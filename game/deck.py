import numpy as np
import copy

from game.player import Player
from typing import Iterable, Optional
from ptypes import Card, Rank, Suit

NUM_CARDS = 52

class PokerDeck:
    def __init__(self, cards: Optional[Iterable[Card]] = None, seed: Optional[int] = None):
        self._cards: tuple[Card]
        self._board: list[Card] = []
        self._cut: int = 0
        
        if cards is None:
            if seed is not None: np.random.default_rng(seed)
            self.shuffle()
        else:
            self._cards = tuple(cards)
            
    def __repr__(self) -> str:
        return "\n".join(self._cards[i].__repr__() + "\n---" if i != 0 and i == self._cut else self._cards[i].__repr__() for i in range(len(self._cards)))
    
    @staticmethod
    def from_cards(cards: Iterable[Card]) -> "PokerDeck":
        assert len(cards) == NUM_CARDS, \
            f"Invalid number of cards: {len(cards)}"
            
        return PokerDeck(cards = cards)
    
    @staticmethod
    def from_seed(seed: int) -> "PokerDeck":
        return PokerDeck(seed = seed)
    
    @property
    def cards(self):
        return self._cards
    
    def copy_cards(self):
        return copy.deepcopy(self._cards)

    @property
    def board(self):
        return self._board
    
    def copy_board(self):
        return self._board.copy()

    def shuffle(self):
        rand_arr = np.arange(NUM_CARDS)
        np.random.shuffle(rand_arr)
        
        self._cards = tuple(
            [Card(rank = Rank(n % 13 + 2), suit = Suit(n % 4)) for n in rand_arr]
        )
        
        self._board.clear()
        
    def deal(self, players: Iterable[Player], count: int = 2):
        if (self._cut != 0): 
            self.shuffle()
        else:
            self._board.clear()
        
        N = len(players)
        
        assert N*count <= NUM_CARDS - 8, \
            f"Too many players: {N}"

        for i, player in enumerate(players):
            player.cards = tuple([self._cards[i + j*N] for j in range(count)])
            
        self._cut = count*N - 1
    
    def step(self):
        assert len(self._board) < 5, "Board full"
            
        # Burn first card
        self._burn()
        
        if len(self._board) == 0:
            # Put three cards on the board for first deal
            for _ in range(3): self._add_to_board()
        else:
            # Otherwise, only add one card
            self._add_to_board()
            
        return self._board.copy()
        
    def _add_to_board(self):
        self._board.append(self._cards[self._cut+1])
        self._cut += 1
        
    def _burn(self): 
        self._cut += 1