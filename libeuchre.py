# libeuchre by Jack Anderson
# a python library for euchre game functions.

from libcards import Hand, Deck, Player, Card, Ace, Jack, Queen, King, Clubs, Diamonds, Hearts, Spades
from helpers import sinput, finput, flip, clear, indexOf, findex, urand

def highest_of_single_suit(cards, trump):
    highest: EuchreCard;
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
    def __init__(self):
        Hand.__init__(self);
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
        
        choice = int(finput(prompt_string, range(1,len(cards)+1), lower=False))
        choice_card = cards[choice-1]
        return choice_card
    def select_suit(self, not_suit):
        trumpopt = []
        for suit in [Clubs, Diamonds, Hearts, Spades]:
            if suit == not_suit:
                continue
            else:
                trumpopt.append(suit)
        
        for i in range(0, len(trumpopt)):
            prompt_string = f"{prompt_string}, ({i+1}) {format_suit(trumpopt[i])}"

        print("choose from suits")
        choice = int(finput(prompt_string, range(1,len(trumpopt)+1), lower=False))
        choise_suit = trumpopt[choice-1]
        return choise_suit
    
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
                elif(call==False):
                    return PreRound1_Result(False, False)  
        else:
            return PreRound1_Result(False, False)
    # preround 2: call trump, or stick to dealer
    def preround_call_trump(self, faceup: Card):     
        print(f"{self.name}'s turn")
        if(self.controlled == True):
            print("Your hand:")
            for card in self.hand.cards:
                print(card.format())
            if(self.dealer == True):
                print("Must select a trump suit")
                suit = self.select_suit(faceup.suit)
                alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                return PreRound2_Result(True, alone, suit)
            else:
                select = finput(f"Select trump? (y/n)", ['y', 'n']) == 'y'
                if select == False:
                    return PreRound2_Result(False)
                else:
                    suit = self.select_suit(faceup.suit)
                    alone = finput(f"Go alone? (y/n)", ['y', 'n']) == 'y'
                    return PreRound2_Result(True, alone, suit)
        else:
            if(self.dealer == True):
                return PreRound2_Result(True, False, urand(1,4,[faceup.card.suit]))
            else:
                return PreRound2_Result(False)
    
    # GAME FUNCTION: NEEDS AUTOMATIC PLAYER CONTROL
    def play_trick(self, lead=None):
        print("Here are your cards:")
        self.hand.display()    
        if lead == None:
            # This player is going first
            card = self.select_card(self.hand.cards)
                
            return CardBundle([card])
        else:
            suit = lead.suit
            cardsofsuit = EuchreHand(self.hand.find_suit(suit))
            if(len(cardsofsuit) > 0):
                print("must follow suit.")
                card = self.select_card(cardsofsuit)
                return CardBundle([card])
            else:
                card = self.select_card(self.hand.cards)
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
        i = 0
        while not self.check_win()[0]:
            # rotate through players for dealers until a team wins
            dealer_index = findex(i, self.players)
            round = Round(deck=self.deck, players=self.players, dealer_index=dealer_index)
            res: RoundResult = round.run()
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
                res: CardBundle = player.play_trick()
                for card in res.cards:
                    player.hand.remove_card(card);
                    self.add_card(card)
                    print(f"${player.name} puts down ${card.format()}")
            else:
                # must follow suit, so pass the lead card
                lead_card = self.cards[0]
                res: CardBundle = player.play_trick(lead_card)          
                for card in res.cards:
                    player.hand.remove_card(card);
                    self.add_card(card)
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
        self.players = players
        self.dealer: EuchrePlayer = self.players[dealer_index]
        # TODO: CHANGE THIS LINE (NOT SURE IF IT HAS A PURPOSE)
        self.dealer.dealer = True
        
        self.deck: Deck = deck
        self.kitty = Hand()
        self.trick_scores = [0,0]
        self.trump = None;
        self.caller: EuchrePlayer = None;
        self.caller_alone: bool = False 
        
    # deal 5 cards to each player
    def deal_cards(self):
        for a in range(0,5):
            # start at player next to the dealer
            for i in range(0,len(self.players)):
                ind = findex(self.start_index+i, self.players)
                player: EuchrePlayer = self.players[ind]
                player.hand.add_card(self.deck.deal())
                
    def deal(self):
        # deal cards to players
        self.deal_cards();
        # add remainder of cards to kiddy
        self.deck.dump(self.kitty)
        # turn up first card of kiddy
        self.kitty.cards[0].visible = True  
        print(f"The top card of the kitty is {self.kitty.cards[0].format()}")
        
    # call to pick up or pass
    def preround(self):
        # start at player next to the dealer
        for i in range(0,len(self.players)):
            ind = findex(self.start_index+i, self.players)
            player = self.players[ind]
            result: PreRound1_Result = player.preround_pickup(self.kitty.cards[0], self.dealer)
            if(result.call == True):
                self.trump = self.kitty.cards[0].suit
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
            player = self.players[ind]
            result: PreRound2_Result = player.preround_call_trump(self.kitty.cards[0], self.dealer)
            if(result.call == True):
                self.trump = result.suit
                self.caller = player
                self.caller_alone = result.alone
                return
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
        
