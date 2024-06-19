from game.deck import PokerDeck
from game.player import Player
from game.table import PokerTable
from ptypes import Blinds

if __name__ == "__main__":
    deck = PokerDeck()
    p1 = Player(is_bot = False)
    p2 = Player(is_bot = True)
    p3 = Player(is_bot = True)
    p4 = Player(is_bot = True)
    
    p1.stack = 100
    p2.stack = 75
    p3.stack = 10
    p4.stack = 50
    
    table = PokerTable([p1, p2, p3, p4], Blinds(1,2))
    table.run()