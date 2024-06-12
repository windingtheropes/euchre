# libeuchre by Jack Anderson
# a python library for euchre game functions.
# this library is to be stripped down to functions and returns for use with graphics

from libcards import Hand, Deck, Player, Card, Ace, Jack, Queen, King, Clubs, Diamonds, Hearts, Spades
from helpers import flip, clear, indexOf, findex, urand, fiinput
from random import randint

def highest_of_single_suit(cards, trump):
    highest: EuchreCard = None;
    for card in cards:
        if not highest:
            highest = card;
            continue
        if card.hierarchical(trump) > highest.hierarchical(trump):
            highest = card
    return highest
def format_suit(suit):
    if suit == Clubs:
        return "Clubs";
    elif suit == Diamonds:
        return "Diamonds"
    elif suit == Hearts:
        return "Hearts"   
    elif suit == Spades:
        return "Spades" 
# given trump, give the other suit
def offsuit(trump):
    if trump == Spades:
        return Clubs
    elif trump == Clubs:
        return Spades
    elif trump == Diamonds:
        return Hearts
    elif trump == Hearts:
        return Diamonds
    
class EuchreCard(Card):
    def __init__(self, c, s):
        Card.__init__(self, c, s);
        self.visible = True
    # based on trump give a heirarchical representation of the card relative to suit
    # meaning
    # non trump: 9=1, 10=2, jack: 3, queen: 4, king: 5, ace: 6
    # trump: 9=1,10=2,queen:3,king:4,ace:5,offs_jack: 6, jack: 7   
    def hierarchical(self, trump):
        if(self.suit == trump or (self.card == Jack and self.suit == offsuit(trump))):
            if self.card == Jack:
                if self.suit == trump:
                    return 7
                elif self.suit == offsuit(trump):
                    return 6
            else:
                if self.card == 9:
                    return 1;
                elif self.card == 10:
                    return 2;
                elif self.card == Queen:
                    return 3;
                elif self.card == King:
                    return 4;
                elif self.card == Ace:
                    return 5;
        else:
            return (1*self.card) - 8
        
# hand specific to euchre: findsuit based on bauers
class EuchreHand(Hand):
    def __init__(self, preload_cards=[]):
        Hand.__init__(self);
        self.cards=[]
        
        # preload cards to the hand if they were specified
        if len(preload_cards) > 0:
            for card in preload_cards:
                self.add_card(card)
    
    # lead with hearts, jack of diamonds and jcak of hearts showed, spades was trump
    def find_suit(self, query_suit, trump):
        ofsuit = []     
        for card in self.cards:
            if(card.card == Jack):
                # skip the jack if it's the left and suit is offsuit, (jack of spades is not a spade when clubs is trump)
                if(offsuit(trump) == query_suit):
                    continue
                # if trump is the suit we're looking for, the two jacks are trump or left trump
                elif(trump == query_suit and (card.suit == trump or card.suit == offsuit(trump))):
                    ofsuit.append(card)
                # if trump is not the query, no special treatment
                elif(trump != query_suit and card.suit == query_suit):
                    ofsuit.append(card)
            elif(card.suit == query_suit):
                ofsuit.append(card)
        return ofsuit
    
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
# cardbundle returned by a player contributing to a trick
class CardBundle:
    def __init__(self, cards):
        self.cards = cards
        
class EuchrePlayer(Player):
    def __init__(self, name, controlled=False):
        Player.__init__(self, name);
        self.hand = EuchreHand()
        self.team = 0;
        self.dealer = False;
        self.controlled = controlled;

class RoundResult:
    def __init__(self, winning_team, points):
        self.winning_team = winning_team
        self.points = points 
        
# euchre base game class
class Game:
    def __init__(self):
        self.deck = Deck(cards=[Ace,9,10,Jack,Queen,King], suits=[Clubs, Diamonds, Hearts, Spades], card=EuchreCard)
        self.scores = [0,0]
        self.round = None;
        self.dealer_index = 0;
        self.players = []
        print("libeuchre by jack anderson")
    
    # for running the game programmatically
    def add_player(self, player):
        if(len(self.players) >= 4) or (player in self.players):
            return
        
        if(len(self.players) == 0):
            player.team = 0
        else:
            prev_player = self.players[len(self.players)-1]
            player.team = flip(prev_player.team)
        self.players.append(player)
        
    # check if there's a winning team
    def check_win(self):
        for i in range(0,len(self.scores)):
            score = self.scores[i]
            if score >= 10:
                return [True, i]
        return [False]       
    # 
    def next_dealer(self):
        self.round = Round(deck=self.deck, players=self.players, dealer_index=self.dealer_index)
        self.dealer_index += 1
        self.dealer_index = findex(self.dealer_index, self.players)

class Trick_result:
    def __init__(self, card, player_id):
        self.card = card
        self.id = player_id

# euchre trick class, extension of hand, holds cards and determines trick winner
class Trick(Hand):
    def __init__(self, trump, players, lead_index):
        Hand.__init__(self);
        self.cards =[]
        # list of what cards what player placed [player_id, card_id]
        self.player_cards = [];
        self.trump = trump
        self.players = players
        # should be an index
        self.lead_index = lead_index
    
    # get which player placed down card
    def get_player_id_from_card(self, card):
        for pc in self.player_cards:
            if pc[1] == card.id:
                return pc[0]
            
    # identifiable cards to the player
    def add_card(self, card: EuchreCard, player: EuchrePlayer):
        if not card in self.cards and not [player.id, card.id] in self.player_cards:
            self.player_cards.append([player.id, card.id])
            self.cards.append(card)
            
    # get winning card and player id
    def winner(self):
        # if there is trump present, ignore the other cards
        if len(self.find_suit(self.trump)) > 0:
            trump_cards = self.find_suit(self.trump)
            highest: EuchreCard = highest_of_single_suit(trump_cards, self.trump)
            return Trick_result(highest, self.get_player_id_from_card(highest))
        else:
            # highest card of suit lead
            suit_cards = self.find_suit(self.cards[0].suit)
            highest: EuchreCard = highest_of_single_suit(suit_cards, self.trump)
            return Trick_result(highest, self.get_player_id_from_card(highest))
    
# euchre round class, handles 5 rounds of tricks
class Round:
    # info pertaining to the euchre round
    def __init__(self, deck: Deck, players, dealer_index):
        self.dealer_index = dealer_index
        self.start_index = self.dealer_index+1
        self.player_turn_index = self.start_index
        self.players = players
        self.dealer: EuchrePlayer = self.players[self.dealer_index]
        
        self.deck: Deck = deck
        self.kitty = EuchreHand()
        self.trick_scores = [0,0]
        self.trump = None;
        self.caller: EuchrePlayer = None;
        self.called_on_round =  0;
        self.test = [];
        self.caller_alone: bool = False 
        
        # clear dealer attribute of all players except for current dealer
        for player in self.players:
            if(player.id == self.dealer.id):
                player.dealer = True
            else: 
                player.dealer = False
    def turnover_kitty(self):
        self.kitty.cards[0].visible = False
    # call on preround 1
    def pr1_call(self, player:EuchrePlayer, alone:bool):
        self.caller = player
        # scenario where must go alone will be forced if it is applicable
        self.caller_alone = self.must_go_alone(player) or alone
        self.called_on_round = 1
        self.trump = self.kitty.cards[0].suit
        
    # dealer picks up based on call or themself
    def pickup(self, discard: EuchreCard):
        self.dealer.hand.add_card(self.kitty.cards[0])
        self.kitty.remove_card(self.kitty.cards[0])
        self.dealer.hand.remove_card(discard)
        self.kitty.add_card(discard)
        
    # return array of callable suits
    def callable_suits(self, as_cards=False):
        trumpopt = []
        for suit in [Clubs, Diamonds, Hearts, Spades]:
            if suit == self.kitty.cards[0].suit:
                continue
            else:
                if(as_cards == True):
                    trumpopt.append(EuchreCard(14, suit))
                else:
                    trumpopt.append(suit)
        
        return trumpopt
    # call on preround 2
    def pr2_call(self, player:EuchrePlayer, alone=False):
        self.caller=player
        self.caller_alone = alone
        self.called_on_round = 2
    def pr2_select_suit(self, suit):
        self.trump = suit
    
    # deal 5 cards to each player
    def deal_cards(self):
        for a in range(0,5):
            # start at player next to the dealer
            for i in range(0,len(self.players)):
                ind = findex(self.start_index+i, self.players)
                player = self.players[ind]
                card = self.deck.deal()
                player.hand.add_card(card)

    def deal(self):
        # deal cards to players
        self.deal_cards();
        
        # add remainder of cards to kiddy
        self.deck.dump(self.kitty)
        # turn up first card of kiddy
        for card in self.kitty.cards:
            card.visible = False
        self.kitty.cards[0].visible = True  
        print(f"The top card of the kitty is {self.kitty.cards[0].format()}")
    def next_pr1_turn(self):
        
        self.player_turn_index += 1
        self.player_turn_index = findex(self.player_turn_index, self.players)
    # call to pick up or pass
    
    def must_go_alone(self, player):
        if(player.team == self.dealer.team):
            return True
        return False
    
    def find_player_by_id(self, id):
        for player in self.players:
            if player.id == id:
                return player

    # postround: clear hands and clear the deck
    def postround(self):
        for plr in self.players:
            plr.hand.clear()
        self.kitty.clear()
        self.deck.relinquish()
        for card in self.deck.cards:
            card.visible = True
        
    def get_score(self):    
        # points calculator
        for t in range(0,2):
            # if team t won the round
            if(self.trick_scores[t] >= 3):
                if(self.trick_scores[t] == 5):
                    if(self.caller_alone == True):
                        # 4 points for all 5 alone
                        return RoundResult(t, 4)
                    else:
                        # 2 points for all 5 as a team
                        return RoundResult(t, 2)
                else:
                    if(self.caller.team != t):
                        # 2 points for euchre
                        return RoundResult(t, 2)
                    else:
                        # 1 point for winning and calling
                        return RoundResult(t, 1)
            # team t did not win
            else:
                continue
        
