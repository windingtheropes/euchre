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
class EuchreDeck(Deck):
    def __init__(self, cards, suits):
        Deck.__init__(self, cards, suits)
                
    # dump the remainder of the deck into a hand        
    def dump(self, hand: Hand):
        for card in self.cards:
            if not card.id in self.dealt:
                hand.add_card(card)     
                self.dealt.append(card.id)
                
class RoundResult:
    def __init__(self, winning_team, points):
        self.winning_team = winning_team
        self.points = points 
        
# euchre base game class
class Game:
    def __init__(self):
        self.deck = EuchreDeck(cards=[1,9,10,11,12,13])
        self.scores = [0,0]
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
    # check if there's a winning team
    def check_win(self):
        for i in range(0,len(self.scores)):
            score = self.scores[i]
            if score >= 10:
                return [True, i]
        return [False]       
     
    def start(self):
        # start the game
        i = 0
        while not self.check_win()[0]:
            fi = indexf(i)
            dealer = self.players[fi]
            round = Round(self.deck, players=self.players, dealer=dealer)
            res = round.run()
            i+=1
        print(f"Team {self.check_win()[1]} wins.")

# euchre trick round class, handles a round of tricks, selecting trump, etc
class Trick_Round():
    def __init__(self, deck, dealer, players):
        self.deck = deck
        self.dealer = dealer
        
        # starting player
        self.starti = indexOf(dealer, self.plyers) + 1
        
        self.center = Hand()
        
        

# euchre round class, handles 5 rounds of tricks
class Round:
    # info pertaining to the euchre round
    def __init__(self, deck: EuchreDeck, players):
        self.players = players
        self.deck = deck
        self.trick_scores = [0,0]
        self.kiddy = Hand()
        self.trump
        self.caller
        self.caller_alone = False 
        pass
    # deal 5 cards to each player
    def deal_cards(self):
        for a in range(0,5):
            for i in range(0,len(self.players)):
                ind = indexf(self.starti+i)
                player = self.players[ind]
                self.deck.deal_to(player);
        
    def run(self):
        # team then score
        self.deal_cards();
        pass

