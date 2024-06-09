# libeuchre by Jack Anderson
# a python library for euchre game functions.
# this library is to be stripped down to functions and returns for use with graphics

# todo: figure out why cards are double dealing.
from libcards import Hand, Deck, Player, Card, Ace, Jack, Queen, King, Clubs, Diamonds, Hearts, Spades
from helpers import sinput, finput, flip, clear, indexOf, findex, urand, fiinput
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
                
    def find_suit(self, suit, trump):
        ofsuit = []     
        for card in self.cards:
            if(card.card == Jack):
                if(card.suit == suit or card.suit == offsuit(trump)):
                    ofsuit.append(card)
            elif(card.suit == suit):
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
        
    # given an array of selectable cards
    def select_card(self, cards):
        prompt_string = "";
        for i in range(0, len(cards)):
            card = cards[i]
            prompt_string = f"{prompt_string}, ({i+1}) {card.format()}"
            
        print("choose from cards")
        choice = fiinput(prompt_string, range(1,len(cards)+1))
        choice_card = cards[choice-1]
        return choice_card
    def select_suit(self, not_suit):
        trumpopt = []
        prompt_string = ""
        for suit in [Clubs, Diamonds, Hearts, Spades]:
            if suit == not_suit:
                continue
            else:
                trumpopt.append(suit)
                
        print("select trump suit")
        for i in range(0, len(trumpopt)):
            prompt_string = f"{prompt_string}, ({i+1}) {format_suit(trumpopt[i])}"

        print("choose from suits")
        choice = fiinput(prompt_string, range(1,len(trumpopt)+1))
        choise_suit = trumpopt[choice-1]
        return choise_suit
    
    def pickup(self, card):
        if(self.controlled == True):
            clear()
            print(f"You're picking up {card.format()}")
            print("Must discard another card. Select.")
            return self.select_card(self.hand.cards)
        else:
            print(f"{self.name} discards a card and picks up {card.format()}.")
            return self.hand.cards[urand(0, len(self.hand.cards)-1, [])]
        
    # THESE FUNCTIONS NEED REORGANIZING!!!!!
    # preround1: tell dealer to pick up or not
    def preround_pickup(self, faceup: EuchreCard, dealer):
        print(f"{self.name}'s turn")
        if(self.controlled == True):
            clear()
            print("Your hand")
            self.hand.display()
            if(self.dealer == True):
                # if dealer, they can pick up or pass to the next preround
                pickup = finput(f"Pick up {faceup.format()}? (y/n)", ['y', 'n']) == 'y'
                if(pickup == True):
                    alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                    return PreRound1_Result(True, alone)
                return PreRound1_Result(False, False)
            else:
                # if not dealer, they can call to pick up or pass
                call = finput(f"Tell dealer to pick up {faceup.format()}? (y/n)", ['y', 'n']) == 'y'  
                alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'  

                if call == True and self.team == dealer.team:
                   if(self.team == dealer.team):
                       print("Must go alone.")
                       alone = True
                return PreRound1_Result(call, alone)  
        else:
            # automatic players always pass :)
            return PreRound1_Result(False, False)
    # preround 2: call trump, or stick to dealer
    def preround_call_trump(self, faceup: EuchreCard):     
        print(f"{self.name}'s turn")
        if(self.controlled == True):
            # temp disp
            clear()
            print("Your hand")
            self.hand.display()
            if(self.dealer == True):
                # stick to dealer, dealer must call trump suit
                print("Must select a trump suit")
                suit = self.select_suit(faceup.suit)
                alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                return PreRound2_Result(True, alone, suit)
            else:
                # player can choose whether or not to call trump suit
                select = finput(f"Select trump? (y/n)", ['y', 'n']) == 'y'
                if select == True:
                    suit = self.select_suit(faceup.suit)
                    alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                    return PreRound2_Result(True, alone, suit)
                else:
                    return PreRound2_Result(False)
        else:
            if(self.dealer == True):
                # if dealer, must call suit its been stuck to them; automatic
                return PreRound2_Result(True, False, urand(1,4,[faceup.suit]))
            else:
                # not dealer automatic skip
                return PreRound2_Result(False)
    
    def play_trick(self, lead=None, trump=None): 
        if lead == None:
            if(self.controlled == True):
                # temp disp
                clear()
                print("Your hand")
                self.hand.display()
                # This player is going first
                card: EuchreCard = self.select_card(self.hand.cards)
                
                return CardBundle([card])
            else:
                # automatically select a random card
                random_index = randint(0,len(self.hand.cards)-1)
                card: EuchreCard = self.hand.cards[random_index]
                return CardBundle([card])
        else:
            suit = lead.suit
            cardsofsuit = EuchreHand(self.hand.find_suit(suit, trump))
            if(len(cardsofsuit.cards) > 0):
                # player must follow suit
                if self.controlled == True:
                    print("must follow suit.")
                    card: EuchreCard = self.select_card(cardsofsuit.cards)
                    return CardBundle([card])
                else:
                    # automatically select a card of suit
                    random_index = randint(0,len(cardsofsuit.cards)-1)
                    card: EuchreCard = cardsofsuit.cards[random_index]
                    return CardBundle([card])
            else:
                if(self.controlled == True):
                    # player can play any card
                    card: EuchreCard = self.select_card(self.hand.cards)
                    return CardBundle([card])
                else:
                    # automatically select a random card
                    random_index = randint(0,len(self.hand.cards)-1)
                    card: EuchreCard = self.hand.cards[random_index]
                    return CardBundle([card])

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
    # for running the game programmatically
    def add_player(self, player):
        if(len(self.players) >= 4) or (player in self.players):
            return
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
    def start(self):
        # start the game
        i = 0
        while not self.check_win()[0]:
            # rotate through players for dealers until a team wins
            dealer_index = findex(i, self.players)
            self.round = Round(deck=self.deck, players=self.players, dealer_index=dealer_index)
            res: RoundResult = self.round.run()
            self.scores[res.winning_team] += res.points
            i+=1
        print(f"Team {self.check_win()[1]} wins.")

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
            
    def run_trick(self):
        # loop through 4 players
        for i in range(0,4):
            ind = findex(self.lead_index+i, self.players)
            player: EuchrePlayer = self.players[ind] 
            if i == 0:
                # whoever goes first doesn't have a suit to follow
                res: CardBundle = player.play_trick(trump=self.trump)
                for card in res.cards:
                    player.hand.remove_card(card);
                    self.add_card(card, player)
                    print(f"${player.name} puts down ${card.format()}")
            else:
                # must follow suit, so pass the lead card
                lead_card = self.cards[0]
                res: CardBundle = player.play_trick(lead_card, trump=self.trump)          
                for card in res.cards:
                    player.hand.remove_card(card);
                    self.add_card(card, player)
                    print(f"${player.name} puts down ${card.format()}")
        return self
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
    def preround(self):
        # start at player next to the dealer
        for i in range(0,len(self.players)):
            ind = findex(self.start_index+i, self.players)
            player: EuchrePlayer = self.players[ind]
            result: PreRound1_Result = player.preround_pickup(self.kitty.cards[0], self.players[self.dealer_index])
            if(result.call == True):
                discard: EuchreCard = self.dealer.pickup(self.kitty.cards[0])
                self.trump = self.kitty.cards[0].suit
                self.kitty.remove_card(self.kitty.cards[0])
                self.kitty.add_card(discard)
                
                self.caller = player
                self.caller_alone = result.alone
                return
            
        # nobody called
        self.preround2()
    
    # call trump or pass, result in stuck to dealer if all pass
    def preround2(self):
        # start at player next to the dealer
        for i in range(0,len(self.players)):
            ind = findex(self.start_index+i, self.players)
            player: EuchrePlayer = self.players[ind]
            result: PreRound2_Result = player.preround_call_trump(self.kitty.cards[0])
            if(result.call == True):
                self.trump = result.suit
                self.caller = player
                self.caller_alone = result.alone
                return
            
    def must_go_alone(self, player):
        if(player.team == self.dealer.team):
            return True
        return False
    
    def find_player_by_id(self, id):
        for player in self.players:
            if player.id == id:
                return player
    def playround(self):
        # loop through 5 hands
        for i in range(1,6):
            # trick is disposable so cards dont matter to be deleted
            winner: Trick_result = Trick(self.trump, self.players, self.start_index).run_trick().winner()
            player: EuchrePlayer = self.find_player_by_id(winner.id)
            print(f"{player.name} wins the trick with {winner.card.format()}")
            # the winner of the trick plays next
            self.start_index = indexOf(self.find_player_by_id(player.id), self.players)
            self.trick_scores[player.team] += 1      
        pass
    # postround: clear hands and clear the deck
    def postround(self):
        for plr in self.players:
            plr.hand.clear()
        self.kitty.clear()
        self.deck.relinquish()
        pass
    def run(self):
        print(f"{self.players[self.dealer_index].name} is dealing.")
        self.deck.shuffle()
        self.deal()
        
        self.preround()
        self.playround()
        self.postround()
        
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
        
