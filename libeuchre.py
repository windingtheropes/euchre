# libeuchre by Jack Anderson
# a python library for euchre game functions.

from libcards import Hand, Deck, Player
from helpers import sinput, finput, flip, clear, indexOf, indexf
from time import sleep

class EuchrePlayer(Player):
    def __init__(self, name, controlled=False):
        Player.__init__(self, name);
        self.team = 0;
        self.dealer = False;
        self.controlled = controlled;
        
# euchre base game class
class Game:
    def __init__(self):
        self.deck = Deck(cards=[1,9,10,11,12,13])
        self.players = []
        
        print("Euchre by Jack Anderson")
        
        sleep(1)
        clear()
        
    # configure player names, teams, control
    def config_players(self):
        team = 0;
        for i in range(1,5):
            controlled = finput(f"Will player {i} be manually controlled? (y/n) ", ['y','n']) == 'y'
            player = EuchrePlayer(f"Player {i}")
            
            if controlled:
                player_name = sinput(f"Enter a name for Player {i}: ")
                player.name = player_name
                player.controlled = True

            print(f"{player.name} has been created. On team {team}. Controlled: {controlled}")
            player.team = team;
            self.players.append(player)
            
            # flip 0 to 1 or 1 to 0
            team = flip(team)
            
            sleep(1)
            clear()
               
    def start():
        # start the game
        
        pass
        

# euchre trick round class, handles a round of tricks, selecting trump, etc
class Trick_Round():
    def __init__(self, deck, dealer, players):
        self.deck = deck
        self.dealer = dealer
        self.players = players
        
        # starting player
        self.starti = indexOf(dealer, self.plyers) + 1
        
        self.center = Hand()
        self.kiddy = Hand()
        self.trump
        self.caller
        self.caller_alone = False
        
    def deal_cards():
        for i in range(0,5):
            ind = indexf()
        pass
        

# euchre round class, handles 5 rounds of tricks
class Round:
    # info pertaining to the euchre round
    def __init__(self, deck):
        self.deck = deck
        self.trick_scores = [0,0]
        pass
    def run(self):
        pass

