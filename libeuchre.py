# libeuchre by Jack Anderson
# a python library for euchre game functions.

from libcards import Hand, Deck, Player
from libhelpers import finput

class EuchrePlayer(Player):
    def __init__(self):
        Player.__init__();
        self.controlled = False;
        
# euchre base game class
class Game:
    def __init__(self):
        self.deck = Deck(cards=[1,9,10,11,12,13])
        self.players = []
        self.config_players()
        
    def config_players(self):
        for i in range(1,5):
            controlled = finput(f"Will player {i} be manually controlled? (y/n) ", ['y','n']) == 'y'
            if controlled:
            
    def start():
        # start the game
        
        pass
        

# euchre trick round class, handles a round of tricks, selecting trump, etc
class Trick_Round(Hand):
    def __init__(self, dealer):
        Hand.__init__(self)    
        self.dealer = dealer

        self.center = Hand()
        self.kiddy = Hand()
        self.trump
        self.caller
        self.caller_alone = False

# euchre round class, handles 5 rounds of tricks
class Round:
    # info pertaining to the euchre round
    def __init__(self):
        self.trick_scores = [0,0]
        pass
    def run(self):
        pass;

