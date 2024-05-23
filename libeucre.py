import random
import time
import math

def id():
    return math.floor(time.time() * random.random())
      
class Card:
    def __init__(self, card, suit):
        self.card = card
        self.suit = suit
        self.id = id()
        
    # clubs, diamonds, hearts, spades
    def format(self):
        c = self.card
        s = self.suit
        if self.card == 1:
            c = "Ace"
        elif self.card > 10:
            if self.card == 11:
                c = "Jack"
            elif self.card == 12:
                c = "Queen"
            elif self.card == 13:
                c = "King"
        if self.suit == 1:
            s = "Clubs"
        elif self.suit == 2:
            s = "Diamonds"
        elif self.suit == 3:
            s = "Hearts"
        elif self.suit == 4:
            s = "Spades"  
        
        return f"{c} of {s}"
class Deck:
    def __init__(self):
        self.cards = []
        self.dealt = []
        
        # generate euchre deck
        for s in range(1,5):
            for c in range(9, 14):
                self.cards.append(Card(c, s))
            self.cards.append(Card(1, s))
    def deal():
        pass
    def shuffle():
        pass
