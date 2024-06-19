import numpy as np

from game.deck import PokerDeck
from game.player import Player
from typing import Iterable
from ptypes import Blinds, Action

class PokerTable:
    def __init__(self, players: int | Iterable[Player], blinds: Blinds) -> None:
        if isinstance(players, int):
            self._players = [Player() for _ in range(players)]
        else:
            self._players = list(players)
            
        self._blinds = blinds

        self._active_players: list[int] = [id(p) for p in self._players]
        self._current_size: int = 0
        self._pot: int = 0
        
        # Initialize deck
        self._deck = PokerDeck()
        
        # Initialize button position
        self._button = 0
        
    @property
    def N(self): return len(self._active_players)

    def from_id(self, id_: int):
        for player in self._players:
            if id_ == id(player): return player
            
        raise ValueError(f"Invalid id: {id_}")
    
    def valid_index(self, idx): 
        return idx % self.N
    
    def set_blinds(self, small: float, big: float):
        self._blinds.small = small
        self._blinds.big = big
    
    def run(self):
        # Setup
        self.setup()
        
        # Open up the action.
        # Button leads when there are < 3 active players. Otherwise, UTG leads. 
        self.gameloop(
            self.circular_reorder(
                self._active_players, 
                self.valid_index(self._button + (3 if self.N > 3 else 0))
            )
        )
    
        # Teardown
        self.finish()
    
    def setup(self):
        # All players at the table left are now active
        self._active_players = [id(p) for p in self._players]
        
        # Current bet size is equivalent to the big blind
        self._current_size = self._blinds.big
        
        # Pot is set at the big + small blinds
        self._pot = self._blinds.total()
                
        # Deal cards to players, starting w/ SB / button+1
        # TODO: clean-up
        self._deck.deal([self.from_id(x) for x in self.circular_reorder(self._active_players, self._button + 1)])
        
        self.from_id(
            self._active_players[self.valid_index(self._button + (1 if self.N > 2 else 0))]
        ).pay_amount(self._blinds.small)
        
        self.from_id(
            self._active_players[self.valid_index(self._button + (2 if self.N > 2 else 1))]
        ).pay_amount(self._blinds.big)
        
    def circular_reorder(self, ls: list, start: int):
        """Re-order starting at given index circularly"""
        if start < 0: start += len(ls)
        return [ls[i % len(ls)] for i in range(start, start + len(ls))]
    
    def gameloop(self, players: list[int]):
        def request_action(subplayers: list[int]):
            for i in range(len(subplayers)):
                if self.N == 1: return
                
                # Get id
                id = subplayers[i]
                
                # Check if player is active
                if id not in self._active_players: 
                    continue

                # Get player info from id
                player = self.from_id(id)
                
                # Get player's action
                print(f"Current bet size: {self._current_size}")
                
                action = self.process_player_response(player.request_chips(self.is_valid), player.amount)
                
                assert action != Action.NULL, "Unexpected behavior"
                
                print(f"Player: {hex(id)}. Action: {action.name}")
                
                if action == Action.FOLD:
                    # Set player as inactive
                    self.set_inactive(id)
                elif action == Action.RAISE:
                    # Get action from rest of the table
                    request_action(self.circular_reorder(subplayers, self.valid_index(i + 1))[:-1])
                    
                    # Get action from aggressor
                    request_action([subplayers[i]])
                                
        while len(self._deck.board) < 5 and self.N > 1:
            print(f"Board: {self._deck.board}")
            request_action(players)
            
            self.reset(players)
            
            for id in players:
                self.from_id(id).amount = 0
                
            self._deck.step()
            
        print(f"Board: {self._deck.board}")
        if self.N == 1:
            print(f"Winner: {self.from_id(self._active_players[0])}")
        else:
            print("Players")
            for id in self._active_players:
                print(self.from_id(id))
               
    def reset(self, players: list[int]):
        self._current_size = 0
        for player in players:
            self.from_id(player).amount = 0
                
    def set_inactive(self, id: int):
        for i in range(self.N):
            if self._active_players[i] == id:
                self._active_players.pop(i)
                return
        
        raise ValueError(f"Player {hex(id)} not found")                 

    def is_valid(self, current_bet: int) -> bool:
        if current_bet == 0: 
            # Check/fold represented as zero
            return True
        elif current_bet < self._current_size:
            print("Bet size too small")
            return False
        elif current_bet > self._current_size and current_bet < 2*self._current_size:
            # TODO: Should not get flagged for all-in bet where this is violated.
            # Current workaround implemented, but shouldn't rely upon it.
            print("Raise too small")
            return False
        else:
            # Any bet > 2x current sizing is valid
            return True
        
    def process_player_response(self, bet: int, amount: int):
        if bet < 0:
            return Action.NULL # invalid bet amount
        elif bet == 0:
            return Action.CHECK if amount == self._current_size else Action.FOLD
        else:
            self._pot += bet
            if amount > self._current_size:
                self._current_size = amount
                return Action.RAISE
            else:
                return Action.CALL
            
    def finish(self):
        print("Closing")
        exit()