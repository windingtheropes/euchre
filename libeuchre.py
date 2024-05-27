# libeuchre by Jack Anderson
# a python library for euchre game functions.

from libcards import Hand, Deck, Player, Card, Ace, Jack, Queen, King, Clubs, Diamonds, Hearts, Spades
from helpers import sinput, finput, flip, clear, indexOf, indexf, urand
from time import sleep

    
class PreRound1_Result:
    def __init__(self, call:bool, alone:bool=False):
        self.call = call
        self.alone = alone
        pass
class PreRound2_Result:
    def __init__(self, call:bool, alone:bool=False, suit:int=0):
        self.call = call
        self.suit = suit
        self.alone = alone
        pass
class CardBundle:
    def __init__(self, cards):
        self.cards = cards
        
class EuchrePlayer(Player):
    def __init__(self, name, controlled=False):
        Player.__init__(self, name);
        self.team = 0;
        self.dealer = False;
        self.controlled = controlled;
    # THESE FUNCTIONS NEED REORGANIZING!!!!!
    # preround1: tell dealer to pick up or not
    def preround_pickup(self, faceup: Card, dealer):
        print(f"{self.name}'s turn")
        if(self.controlled == True):
            print("Your hand:")
            for card in self.hand.cards:
                print(card.format())
            if(self.dealer == True):
                pickup = finput(f"Pick up {faceup.format()}? (y/n)", ['y', 'n']) == 'y'
                if(pickup == True):
                    alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                    return PreRound1_Result(True, alone)
                return PreRound1_Result(False, False)
            else:
                call = finput(f"Tell dealer to pick up {faceup.format()}? (y/n)", ['y', 'n']) == 'y'  
                if(call == True):
                   if(self.team == dealer.team):
                       print("Must go alone.")
                       return PreRound1_Result(True, True)  
        else:
            return PreRound1_Result(False, False)
    # preround 2: call trump, or stick to dealer
    def preround_call_trump(self, faceup: Card, dealer):
        trumpopt = []
        for i in range(1,5):
            if(i == faceup.suit):
                continue
            else:
                trumpopt.append(str(i))
                
        print(f"{self.name}'s turn")
        if(self.controlled == True):
            print("Your hand:")
            for card in self.hand.cards:
                print(card.format())
            if(self.dealer == True):
                print("Must select a trump suit")
                suit = int(finput(f"Select suit. ({str(trumpopt)})", trumpopt))
                alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                return PreRound2_Result(True, alone, suit)
            else:
                select = finput(f"Select trump? (y/n)", ['y', 'n']) == 'y'
                if select == False:
                    return PreRound2_Result(False)
                else:
                    suit = int(finput(f"Pick up {faceup.format()}? ({str(trumpopt)})", trumpopt))
                    alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                    return PreRound2_Result(True, alone, suit)
        else:
            if(self.dealer == True):
                return PreRound2_Result(True, False, urand(1,4,[faceup.card.suit]))
            else:
                return PreRound2_Result(False)
    
    # GAME FUNCTION
    def play_trick(self, lead=None):
        print("Here are your cards:")
        self.hand.display()    
        if lead == None:
            # This player is going first
            c = int(finput(f"Select a card to lay down (0-${len(self.cards)-1})"), range(0, len(self.cards)))
            card = self.cards[c]
            return CardBundle([card])
        else:
            suit = lead.suit
            cardsofsuit = Hand(self.hand.find_suit(suit))
            if(len(cardsofsuit) > 0):
                print("must follow suit.")
                cardsofsuit.display()
                c = int(finput(f"Select a card to lay down (0-${len(cardsofsuit.cards)-1})"), range(0, len(cardsofsuit.cards)))
                card = cardsofsuit[c]
                return CardBundle([card])
            else:
                c = int(finput(f"Select a card to lay down (0-${len(self.cards)-1})"), range(0, len(self.cards)))
                card = self.cards[c]
                return CardBundle([card])
class EuchreDeck(Deck):
    def __init__(self, cards=[Ace,2,3,4,5,6,7,8,9,10,Jack,Queen,King], suits=[Clubs,Diamonds,Hearts,Spades]):
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
        self.deck = EuchreDeck(cards=[Ace,9,10,Jack,Queen,King])
        self.scores = [0,0]
        self.players = []
        
        print("Euchre by Jack Anderson")
        
        
        
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
            
            
    # check if there's a winning team
    def check_win(self):
        for i in range(0,len(self.scores)):
            score = self.scores[i]
            if score >= 10:
                return [True, i]
        return [False]       
     
    def start(self):
        # start the game
        # i = 0
        # while not self.check_win()[0]:
        fi = indexf(0, self.players)
        dealer_index = fi
        round = Round(deck=self.deck, players=self.players, dealer_index=dealer_index)
        res = round.run()
        # i+=1
        # print(f"Team {self.check_win()[1]} wins.")

class Trick_result:
    def __init__(self, card, player_id):
        self.card = card

# euchre trick class, extension of hand, holds cards and determines trick winner
class Trick(Hand):
    def __init__(self, trump, players, lead_index):
        Hand.__init__(self);
        self.trump = trump
        self.players = players
        # should be an index
        self.lead_index = lead_index
    def run_trick(self):
        # loop through 4 players
        for i in range(0,4):
            ind = indexf(self.lead_index+i, self.players)
            player = self.players[ind] 
            if i == 0:
                # whoever goes first doesn't have a suit to follow
                res = player.play_trick()
            else:
                # must follow suit, so pass the lead card
                lead_card = self.cards[0]
                res = player.play_trick(lead_card)          
        pass;    
    # identifiable cards to the player
    def add_card(self, card, player):
        if not [card, player.id] in self.cards:
            self.cards.append([card, player.id])
    # get winning card and player id
    def winner():
        pass   
    
        
        

# euchre round class, handles 5 rounds of tricks
class Round:
    # info pertaining to the euchre round
    def __init__(self, deck: EuchreDeck, players, dealer_index):
        self.dealer_index = dealer_index
        self.start_index = self.dealer_index+1
        self.players = players
        self.dealer = self.players[dealer_index]
        self.dealer.dealer = True
        
        self.deck = deck
        self.kiddy = Hand()
        self.trick_scores = [0,0]
        self.trump = None;
        self.caller = None;
        self.caller_alone = False 
        
    # deal 5 cards to each player
    def deal_cards(self):
        for a in range(0,5):
            # start at player next to the dealer
            for i in range(0,len(self.players)):
                ind = indexf(self.start_index+i, self.players)
                player: EuchrePlayer = self.players[ind]
                player.hand.add_card(self.deck.deal())
                
    def deal(self):
        # deal cards to players
        self.deal_cards();
        # add remainder of cards to kiddy
        self.deck.dump(self.kiddy)
        # turn up first card of kiddy
        self.kiddy.cards[0].visible = True  
        print(f"The top card of the kiddy is {self.kiddy.cards[0].format()}")
        
    # call to pick up or pass
    def preround(self):
        # start at player next to the dealer
        for i in range(0,len(self.players)):
            ind = indexf(self.start_index+i, self.players)
            player = self.players[ind]
            result: PreRound1_Result = player.preround_pickup(self.kiddy.cards[0], self.dealer)
            if(result.call == True):
                self.trump = self.kiddy.cards[0].suit
                self.caller = player
                self.caller_alone = result.alone
                return
        # nobody called
        self.preround2()
    
    # call trump or pass, result in stuck to dealer if all pass
    def preround2(self):
        # start at player next to the dealer
        for i in range(0,len(self.players)):
            ind = indexf(self.start_index+i, self.players)
            player = self.players[ind]
            result: PreRound2_Result = player.preround_call_trump(self.kiddy.cards[0], self.dealer)
            if(result.call == True):
                self.trump = result.suit
                self.caller = player
                self.caller_alone = result.alone
                return
    
    def playround(self):
        # loop through 5 hands
        for i in range(1,6):
            winner = Trick(self.trump, self.players, self.start_index)
            pass      
        pass
    # postround: clear hands and clear the deck
    def postround(self):
        for plr in self.players:
            plr.hand.clear()
        self.kiddy.clear()
        self.deck.relinquish()
        pass
    def run(self):
        print(f"{self.players[self.dealer_index].name} is dealing.")
        self.deck.shuffle()
        self.deal()
        
        self.preround()
        self.playround()
        
