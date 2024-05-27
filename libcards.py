# libcards by Jack Anderson
# a python library for card games.

from helpers import generate_id, log, urand

# suits
Clubs = 1
Diamonds = 2
Hearts = 3
Spades = 4

# face cards
Jack = 11
Queen = 12
King = 13
Ace = 1

# Player base class, contains a hand
class Player:
    def __init__(self, name):
        self.name = name
        self.id = generate_id()
        self.hand = Hand()
# Card class, contains a card number, a suit, and a unique id
class Card:
    def __init__(self, card, suit, visible=False):
        self.card = card
        self.suit = suit
        self.visible = visible
        self.id = generate_id()
    
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

# Hand base class, contains an array of cards
class Hand:
    def __init__(self):
        self.cards = []
    def add_card(self, card):
        if card in self.cards:
            log("Card exists in hand already. Not added.")
        else:
            self.cards.append(card)
    # remove a card from the hand. ** NOTE: NOT THE SAME AS RETURING TO THE DECK
    def remove_card(self, card):
        newcards = []
        if not card in self.cards:
            log("Card not in hand. Not removed.")
        else:
            self.cards.remove(card)
    # move a card to another hand (after dealing)
    def move_card(self, card, hand):
        hand.add_card(card)
        self.remove_card(card)
            
# Deck class, contains an array 
class Deck:
    def __init__(self, cards=[Ace,2,3,4,5,6,7,8,9,10,Jack,Queen,King], suits=[Clubs,Diamonds,Hearts,Spades]):
        self.cards = []
        self.dealt = []

        # Fill the deck according to card restraints
        for s in suits:
            for c in cards:
                self.cards.append(Card(c, s))
                
    # pull a card from the top of the undealt deck
    def deal(self):
        if len(self.dealt) == len(self.cards):
            return print("Deck is out of cards")
        for card in self.cards:
            if card.id in self.dealt:
                continue
            else:
                self.dealt.append(card.id)
                return card
    # return all cards to the deck (clear self.dealt)
    def relinquish(self):    
        self.dealt = []
    
    # shuffle the deck
    def shuffle(self):
        newdeck = []
        reps = []
        # loop through number of cards to ensure every card is reassigned a position
        for i in range(0, len(self.cards)):
            r, reps = urand(0, len(self.cards)-1, reps)
            newdeck.append(self.cards[r])
        self.cards = newdeck
        

    

