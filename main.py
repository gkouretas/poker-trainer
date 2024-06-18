from deck import PokerDeck
from player import Player

if __name__ == "__main__":
    deck = PokerDeck()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    p4 = Player()
    
    deck.deal((p1, p2, p3, p4))
    print(deck)
    print(p1, p2, p3, p4)
    for _ in range(3):
        print(deck.step())