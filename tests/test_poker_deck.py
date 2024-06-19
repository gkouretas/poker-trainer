import unittest

# TODO: fix imports
import sys
sys.path.append("../")

from game.deck import PokerDeck
from game.player import Player

class TestPokerDeck(unittest.TestCase):
    def setUp(self):
        """Constructor for poker deck"""
        self.deck = PokerDeck()
    
    def test_construction(self):
        """Test whether a valid card configuration is made upon construction"""
        cards: list[str] = []
        
        # Test for uniqueness of all the cards
        for card in self.deck.cards:
            decoded_card = bin((card.rank.value << 2) | card.suit.value)
            for c in cards:
                self.assertFalse(c == decoded_card)
            cards.append(decoded_card)
            
    def test_shuffle(self):
        # Get copy of existing cards
        original_cards = self.deck.copy_cards()
        
        # Re-shuffle
        self.deck.shuffle()
        
        # Get updated cards
        new_cards = self.deck.cards
        
        # Verify cards are not equal
        self.assertNotEqual(original_cards, new_cards)
        
        # Re-test construction to verify all cards are unique
        self.test_construction() 
        
    def test_deal(self):
        # Initialize players
        p1 = Player()
        p2 = Player()
        p3 = Player()
        
        # Deal 3-handed, 2 cards
        N = 3
        self.deck.deal((p1, p2, p3), count = 2)
        self.assertTrue(len(p1.cards) == 2)
        self.assertTrue(self.deck.cards[0] in p1.cards)
        self.assertTrue(self.deck.cards[N] in p1.cards)
        
        self.assertTrue(len(p2.cards) == 2)
        self.assertTrue(self.deck.cards[1] in p2.cards)
        self.assertTrue(self.deck.cards[N+1] in p2.cards)

        self.assertTrue(len(p3.cards) == 2)
        self.assertTrue(self.deck.cards[2] in p3.cards)
        self.assertTrue(self.deck.cards[N+2] in p3.cards)
        
        # Deal 2-handed, 4 cards
        N = 2
        self.deck.deal((p1, p2), count = 4)
        self.assertTrue(len(p1.cards) == 4)
        self.assertTrue(self.deck.cards[0] in p1.cards)
        self.assertTrue(self.deck.cards[N] in p1.cards)
        self.assertTrue(self.deck.cards[2*N] in p1.cards)
        self.assertTrue(self.deck.cards[3*N] in p1.cards)
        
        self.assertTrue(len(p2.cards) == 4)
        self.assertTrue(self.deck.cards[1] in p2.cards)
        self.assertTrue(self.deck.cards[N+1] in p2.cards)
        self.assertTrue(self.deck.cards[2*N+1] in p2.cards)
        self.assertTrue(self.deck.cards[3*N+1] in p2.cards) 
        
        # Extreme case: run round w/ max # of players w/o erroring
        self.deck.deal(tuple([Player()] * 22),2)
        for _ in range(3): self.deck.step()
        
        # Raises assertation if too many players are attempted to be added
        self.assertRaises(AssertionError, self.deck.deal, tuple([Player()] * 23),2,)       

    def test_burn(self):
        # Record initial cut index
        starting_cut = self.deck._cut
        
        # Verify cut index increments after burn
        self.deck._burn()
        self.assertEqual(starting_cut + 1, self.deck._cut)

    def test_step(self):
        # Board is initially empty
        self.assertListEqual(self.deck.board, [])
        
        # Record initial cut index
        starting_cut = self.deck._cut
        
        # Verify 3 cards get dealt
        self.deck.step()
        self.assertListEqual(
            self.deck.board, 
            [self.deck.cards[starting_cut+2],self.deck.cards[starting_cut+3],self.deck.cards[starting_cut+4]]
        )
        
        # Verify 1 more card gets dealt, with burn being applied
        self.deck.step()
        self.assertListEqual(
            self.deck.board, 
            [self.deck.cards[starting_cut+2],self.deck.cards[starting_cut+3],self.deck.cards[starting_cut+4],self.deck.cards[starting_cut+6]]
        )
        
        # Verify 1 more card gets dealt, with burn being applied
        self.deck.step()
        self.assertListEqual(
            self.deck.board, 
            [self.deck.cards[starting_cut+2],self.deck.cards[starting_cut+3],self.deck.cards[starting_cut+4],self.deck.cards[starting_cut+6],self.deck.cards[starting_cut+8]]
        )
        
        # Verify no more cards are dealt when board is full
        self.assertRaises(AssertionError, self.deck.step)
        self.assertListEqual(
            self.deck.board, 
            [self.deck.cards[starting_cut+2],self.deck.cards[starting_cut+3],self.deck.cards[starting_cut+4],self.deck.cards[starting_cut+6],self.deck.cards[starting_cut+8]]
        )
        
        # Board clears upon re-shuffle
        self.deck.shuffle()
        self.assertListEqual(self.deck.board, [])
        
if __name__ == '__main__':
    unittest.main()
