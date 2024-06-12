import pygame
from helpers import flip, findex, indexOf
from libeuchre import Game, EuchrePlayer, Round, Trick, Trick_result, EuchreCard, RoundResult, format_suit

pygame.init()

WIDTH = 1382
HEIGHT = 778
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Euchre")

def font(font, size):
    return pygame.font.SysFont(font, size)
futura128 = font("Futura", 128)
futura64 = font("Futura", 64)
futura48 = font("Futura", 48)
futura32 = font("Futura", 32)

class CardDisplay:
    def __init__(self, coords=(0,0), selectable=False):
        self.cards = []
        self.selectable = selectable
        self.selected = 0;
        self.x, self.y = coords
        self.width = 222;
        self.height = 323;
        self.card_imgs = []
    def load(self):
        for card in self.cards:
            c = None
            if(card.visible == False):
                c = pygame.image.load("img/back.png") 
            else:
                c = pygame.image.load(f"img/{card.format().lower().replace(' ', '_')}.png")
            # dimensions of any given card is 222x323, so this is half scale
            c = pygame.transform.scale(c, (self.width/2,self.height/2))
            self.card_imgs.append(c)
            
    def render(self, s=screen):
        # for e in pygame.event.get(): self.event(e)
        x = self.x
        # print(self.selected)
        for i in range(0, len(self.card_imgs)):
            cimg = self.card_imgs[i]
            s.blit(cimg, (x,self.y))
            x+=self.width/2
        if(self.selectable == True):
            # indicate selected card by a red line under it
            pygame.draw.rect(s, (255,0,0), pygame.Rect(self.x+(self.selected*(222/2)),self.y+(323/2),(222/2),10))
    # if the selectable trait is true, arrow keys will change selected card
    def event(self, e):
        if(self.selectable == True):
            if(e.type == pygame.KEYDOWN):
                if(e.key == pygame.K_RIGHT):
                    self.selected = findex(self.selected+1, self.cards, cap=True)
                if(e.key == pygame.K_LEFT):
                    self.selected = findex(self.selected-1, self.cards, ignore_negatives=True)
                    
    def set_cards(self,cards):
        self.cards = cards
        self.card_imgs = []
        self.selected = 0
        self.load()
   
class Flow:
    def __init__(self):
        pass
    def render(self):
        pass
    def event(self, e):
        pass;

# render item to xy at its center
def offsetblit(obj, surf, x=0, y=0):
    obj_offset_height = obj.get_height()/2
    obj_offset_width = obj.get_width()/2
    surf.blit(obj, (-obj_offset_width+x, -obj_offset_height+y))

class MainScreen(Flow):
    def __init__(self):
        self.alive = True
        pass
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura128.render("Euchre", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        
        authorSubtitle = futura48.render("by Jack Anderson", True, (0,0,0))
        offsetblit(authorSubtitle, screen, x=(WIDTH/2), y=(HEIGHT/2)+100)
        
        playButton = futura64.render("Press Enter to start", True, (0,255,50))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
        pass;
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.alive = False
                return

class PlayerSelectScreen(Flow):
    def __init__(self, game):
        self.alive = True
        self.player = 1;
        self.game: Game = game
        # 0= auto 1= next
        self.selectedButton = 1;
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura48.render("Euchre", True, (0,0,0))
        screen.blit(euchreTitle, (0,0))
        
        euchreTitle = futura48.render(f"Player {self.player}", True, (0,0,0))
        screen.blit(euchreTitle, (WIDTH-euchreTitle.get_width(),0))
        
        euchreTitle = futura48.render(f"Use arrow keys to select, then press enter", True, (0,0,0))
        screen.blit(euchreTitle, (WIDTH/2-euchreTitle.get_width()/2,HEIGHT/2-euchreTitle.get_height()))
        
        nextButton = futura48.render("Real Player", True, (0,0,0))
        autoButton = futura48.render("Automatic Player", True, (0,0,0))

        if(self.selectedButton == 1):
            nextButton = futura48.render("Real Player", True, (0,0,0),(0,255,100))
        elif(self.selectedButton == 0):
            autoButton = futura48.render("Automatic Player", True, (0,0,0),(0,255,100))
        
        
        screen.blit(nextButton, (WIDTH-nextButton.get_width(), HEIGHT-nextButton.get_height()))
        screen.blit(autoButton, (0, HEIGHT-autoButton.get_height()))
       
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                if(self.player <= 4):
                    controlled = self.selectedButton == 1
                    self.game.add_player(EuchrePlayer(name=f"Player {self.player}",controlled=controlled))
                    print(f"Player {self.player} added")
                    if(self.player+1 > 4):
                        self.alive = False
                    else: 
                        self.player+=1
                else:
                    self.alive = False
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                self.selectedButton = flip(self.selectedButton)
class PregameScreen(Flow):
    def __init__(self):
        self.alive = True
        pass
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura128.render("Euchre", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        
        playButton = futura64.render("Press Enter to continue", True, (0,50,255))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
        pass;
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.alive = False
                return

class EnterSplash(Flow):
    def __init__(self, text=""):
        self.text = text;
        self.alive = True
        
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura48.render(self.text, True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        
        playButton = futura64.render("Press Enter to continue", True, (0,50,255))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.alive = False
                return
       
class Preround1Screen(Flow):
    def __init__(self, screen):
        self.screen = screen
        self.alive = True
        self.result = None;
        # 1 is call 0 is pass
        self.selectedButton = 0;
        self.kitty_display = CardDisplay((0, HEIGHT/2))
        self.hand_display = CardDisplay((0,50))
    def render(self):
        player = self.screen.game.players[findex(self.screen.player_rot_i, self.screen.game.players)]
        
        euchreTitle = futura48.render(f"{player.name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions = futura32.render(f"Use arrow keys to select, then press enter", True, (0,0,0))
        offsetblit(instructions, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        
        kittyTitle = futura32.render("Kitty", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        self.kitty_display = CardDisplay((0, HEIGHT/2))
        self.kitty_display.set_cards([self.screen.game.round.kitty.cards[0]])
        self.kitty_display.render()
        
        handTitle = futura32.render("Your hand", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        self.hand_display.set_cards(player.hand.cards)
        self.hand_display.render()
        
        handTitle = futura32.render(f"{self.screen.game.round.dealer.name} dealt.", True, (0,0,0))
        screen.blit(handTitle, (WIDTH-handTitle.get_width(), 0))
        
        callButton = futura48.render("Call", True, (0,0,0))
        passButton = futura48.render("Pass", True, (0,0,0))

        if(self.selectedButton == 1):
            callButton = futura48.render("Call", True, (0,0,0),(255,0,50))
        elif(self.selectedButton == 0):
            passButton = futura48.render("Pass", True, (0,0,0),(0,255,100))
        
        
        screen.blit(passButton, (WIDTH-passButton.get_width(), HEIGHT-passButton.get_height()))
        screen.blit(callButton, (0, HEIGHT-callButton.get_height()))
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                self.selectedButton = flip(self.selectedButton)
            if e.key == pygame.K_RETURN:
                if self.selectedButton == 0:
                    # pass
                    self.alive = False
                    self.result = 0
                elif self.selectedButton == 1:
                    # call to pickup
                    self.alive = False;
                    self.result = 1
                 
class PickupScreen(Flow):
    def __init__(self, screen):
        self.screen = screen
        self.game: Game = self.screen.game
        self.alive = True
        self.result = None;
        self.player: EuchrePlayer = None;
        self.hand_display = CardDisplay((0,50), selectable=True)
        self.kitty_display = CardDisplay((0, HEIGHT/2))
        # 1 is call 0 is pass
        self.initialized = False
        self.selectedButton = 0;
        
    def initialize(self):
        self.player = self.game.round.dealer
        self.kitty_display.set_cards([self.game.round.kitty.cards[0]])
        self.hand_display.set_cards(self.player.hand.cards)
        
    def render(self):
        if(self.initialized == False):
            self.initialize()
            self.initialized = True
    
        euchreTitle = futura48.render(f"{self.player.name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions1 = futura32.render(f"Picking up {self.game.round.kitty.cards[0].format()}. Must discard a card.", True, (0,0,0))
        offsetblit(instructions1, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        instructions2 = futura32.render(f"Use arrow keys to select a discard, then press enter", True, (0,0,0))
        offsetblit(instructions2, screen, x=(WIDTH/2), y=(HEIGHT/2)+100)
        
        kittyTitle = futura32.render("Kitty", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        
        self.kitty_display.render()
        
        handTitle = futura32.render("Your hand:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        self.hand_display.render()
        
        handTitle = futura32.render(f"{self.game.round.dealer.name} dealt.", True, (0,0,0))
        screen.blit(handTitle, (WIDTH-handTitle.get_width(), 0))
        
        
    def event(self, e):
        self.hand_display.event(e)
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_RETURN):
                self.game.round.pickup(self.game.round.dealer.hand.cards[self.hand_display.selected])
                self.alive = False
                
class SelectTrumpScreen(Flow):
    def __init__(self, screen):
        self.screen = screen
        self.game: Game = self.screen.game
        self.alive = True
        # follows suit enum
        self.result = None;
        self.player: EuchrePlayer = None;
        self.hand_display = CardDisplay((0,50))
        self.choices_display = CardDisplay((0, HEIGHT/2), selectable=True)
        # 1 is call 0 is pass
        self.initialized = False
        # self.selectedButton = 0;
        
    def initialize(self):
        self.player = self.game.players[indexOf(self.game.round.caller, self.game.players)]
        print(self.game.round.caller.name)
        self.choices_display.set_cards(self.game.round.callable_suits(as_cards=True))
        self.hand_display.set_cards(self.player.hand.cards)
        
    def render(self):
        # don't know why i have to do this
        # if(self.alive == False):
        #     return
        if(self.initialized == False):
            self.initialize()
            self.initialized = True
    
        euchreTitle = futura48.render(f"{self.player.name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions1 = futura32.render(f"Calling trump.", True, (0,0,0))
        offsetblit(instructions1, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        instructions2 = futura32.render(f"Use arrow keys to select a suit, then press enter", True, (0,0,0))
        offsetblit(instructions2, screen, x=(WIDTH/2), y=(HEIGHT/2)+100)
        
        kittyTitle = futura32.render("Options", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        
        self.choices_display.render()
        
        handTitle = futura32.render("Your hand:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        self.hand_display.render()
        
        handTitle = futura32.render(f"{self.game.round.dealer.name} dealt.", True, (0,0,0))
        screen.blit(handTitle, (WIDTH-handTitle.get_width(), 0))
        
        
    def event(self, e):
        self.choices_display.event(e)
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_RETURN):
                self.game.round.pr2_select_suit(self.choices_display.cards[self.choices_display.selected].suit) 
                self.alive = False
 
class Preround2Screen(Flow):
    def __init__(self, screen):
        self.screen = screen
        self.alive = True
        self.result = None;
        # 1 is call 0 is pass
        self.selectedButton = 0;
        
    def render(self):
        player = self.screen.game.players[findex(self.screen.player_rot_i, self.screen.game.players)]
        
        euchreTitle = futura48.render(f"{player.name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions = futura32.render(f"Use arrow keys to select, then press enter", True, (0,0,0))
        offsetblit(instructions, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        
        kittyTitle = futura32.render("Kitty", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        kd = CardDisplay((0, HEIGHT/2))
        kd.set_cards([self.screen.game.round.kitty.cards[0]])
        kd.render()
        
        handTitle = futura32.render("Your hand", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        c = CardDisplay((0,50))
        c.set_cards(player.hand.cards)
        c.render()
        
        handTitle = futura32.render(f"{self.screen.game.round.dealer.name} dealt.", True, (0,0,0))
        screen.blit(handTitle, (WIDTH-handTitle.get_width(), 0))
        
        callButton = futura48.render("Call", True, (0,0,0))
        passButton = futura48.render("Pass", True, (0,0,0))

        if(player.id == self.screen.game.round.dealer.id):
            print("dealer, must call")
            self.result = 1
            self.alive = False
            
        if(self.selectedButton == 1):
            callButton = futura48.render("Call", True, (0,0,0),(255,0,50))
        elif(self.selectedButton == 0):
            passButton = futura48.render("Pass", True, (0,0,0),(0,255,100))
        
        
        screen.blit(passButton, (WIDTH-passButton.get_width(), HEIGHT-passButton.get_height()))
        screen.blit(callButton, (0, HEIGHT-callButton.get_height()))
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                self.selectedButton = flip(self.selectedButton)
            if e.key == pygame.K_RETURN:
                if self.selectedButton == 0:
                    # pass
                    self.alive = False
                    self.result = 0
                elif self.selectedButton == 1:
                    # call to pickup
                    self.alive = False;
                    self.result = 1
       
# screen to handle all preround  
class PreroundScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.alive = True
        self.card_display = CardDisplay()
        
        # meta round
        self.round_initialized = False
        self.dealer_rot_i = self.game.dealer_index;
        
        # round
        self.player_rot_i = self.dealer_rot_i+1;

        # pickup call round
        # meta active, prerender
        self.pickupround_active = True
        self.preround1_i = 0;
        self.pickupround_screen = Preround1Screen(self)
        
        # dealer pickup?
        self.pickup_active = False
        self.pickup_screen = PickupScreen(self)
        # we don't actually need to know what card the player discarded
        
        # trump call round?
        self.preround2_active = False
        self.preround2_o = 0;
        self.preround2_screen = Preround2Screen(self)
        # will need to parse result of call
        self.select_trump_active = False
        self.select_trump_screen = SelectTrumpScreen(self);
        self.preround2_i = 0
    def reset(self):
        self.__init__(self.game)
    def init__round(self):
        # initialize the round, deck
        if self.round_initialized == False:
            self.game.round = Round(self.game.deck, self.game.players, findex(self.dealer_rot_i, self.game.players))
            self.game.deck.shuffle()
            self.game.round.deal()
            self.dealer_rot_i += 1;
            
        self.round_initialized = True
    
    def preround1(self):
        if(self.pickupround_active == True):
            self.pickupround_screen.render() 
        # if the pickupround screen is finished, but the pickupround results havent been handled yet, as indicated by self.pickupround_active
        if(self.pickupround_screen.alive == False and self.pickupround_active == True):
            player = self.game.players[findex(self.player_rot_i, self.game.players)]    
            # player is not dealer, not on 4th player so not the dealer
            if(player.id != self.game.round.dealer.id) and self.preround1_i < 3:
                if(self.pickupround_screen.result == 1):
                    # a player calls
                    self.game.round.pr1_call(player, False)
                else:
                    # a player passes
                    pass
                
                # the player just called, cut the round
                if(self.game.round.called_on_round == 1):
                    self.pickupround_active = False
                else:
                    self.preround1_i += 1
                    self.player_rot_i += 1
                    self.pickupround_screen.alive = True
                
            # player is dealer on 3rd round and that makes sense :)
            elif(player.id == self.game.round.dealer.id) and self.preround1_i == 3:
                if(self.pickupround_screen.result == 1):
                    # dealer calls to pick up
                    self.game.round.pr1_call(player, False)
                else:
                    # dealer passes and preround 2 is needed
                    self.game.round.turnover_kitty()
                    # pass current dealer index
                    self.player_rot_i = self.game.round.dealer_index+1;
                    self.preround2_active = True
                self.pickupround_active = False   
        if(self.game.round.called_on_round == 1):
            self.pickup_active = True
    def pickup(self):
        if(self.pickup_screen.alive == False):
            self.pickup_active = False;
        if(self.pickup_active == True and self.pickup_screen.alive == True):
            self.pickup_screen.render()   

    def preround2(self):
        if(self.game.round.called_on_round == 2):
            self.preround2_active = False
            self.select_trump_active = True
            # self.select_trump_active = True
        if(self.preround2_active == True and self.preround2_screen.alive == True and self.game.round.called_on_round == 0):
            self.preround2_screen.render()
        if(self.preround2_screen.alive == False and self.preround2_active == True and self.game.round.called_on_round == 0):
            player = self.game.players[findex(self.player_rot_i, self.game.players)]    
            # player is not dealer, not on 4th player so not the dealer
            if(player.id != self.game.round.dealer.id) and self.preround2_i < 3:
                if(self.preround2_screen.result == 1):
                    # a player calls
                    self.game.round.pr2_call(player, alone=False)
                    self.preround2_active = False
                    self.select_trump_active = True
                else:
                    self.preround2_i += 1
                    self.player_rot_i += 1
                    self.preround2_screen.alive = True
                    # a player passes
                
            # player is dealer on 3rd round and that makes sense :)
            elif(player.id == self.game.round.dealer.id) and self.preround2_i == 3:
                # stuck to dealer
                self.game.round.pr2_call(player, alone=False)
                self.preround2_active = False   
                self.select_trump_active = True
        
    def select_trump(self):
        if(self.select_trump_active == True and self.select_trump_screen.alive == True):
            self.select_trump_screen.render()
        if(self.select_trump_screen.alive == False):
            self.select_trump_active = False
    
    def render(self):
        self.init__round()
        screen.fill((255,255,255))
        
        
        self.preround1()
        # this will only run if preround1 needs it to
        self.pickup()  
        # this will only run if needed
       
        self.preround2() 
        self.select_trump()
        
        if(self.game.round.called_on_round != 0 and self.pickupround_active == False and self.pickup_active == False and self.preround2_active == False and self.select_trump_active == False):
            # preround is over. all round info is generated
            self.alive = False
        
    def event(self,e):
        if(self.pickupround_active == True):
            self.pickupround_screen.event(e)
        if(self.pickup_active == True):
            self.pickup_screen.event(e)
        if(self.preround2_active == True):
            self.preround2_screen.event(e)
        if(self.select_trump_active == True):
            self.select_trump_screen.event(e)

# keep in mind this is rendering on a display -211 y
class PlayerTrickSelectScreen(Flow):
    def __init__(self, screen):
        self.screen: TrickScreen = screen
        self.game: Game = self.screen.game
        self.alive = True
        self.result = None;
        self.player: EuchrePlayer = None;
        self.hand_display = CardDisplay((0,50))
        self.selectable_display = CardDisplay((0, (HEIGHT/2)), selectable=True)
        # 1 is call 0 is pass
        self.initialized = False
        self.rel_height = HEIGHT -211
    def reset(self):
        self.initialized = False
        self.player = None
        self.result = None
        self.alive = True
        
    def initialize(self):
        self.player = self.game.players[findex(self.screen.player_turn_i+self.screen.screen.lead_player_index, self.game.players)]
        # leader can play any card
        if(self.screen.player_turn_i == 0):
            self.selectable_display.set_cards(self.player.hand.cards)
        elif(self.screen.player_turn_i < 4):
            lead_card = self.screen.trick.cards[0]
            cards_of_suit = self.player.hand.find_suit(lead_card.suit, self.screen.game.round.trump)
            # must follow suit if suit is found otherwise any card
            if(len(cards_of_suit) > 0):
                self.selectable_display.set_cards(cards_of_suit)
            else:
                self.selectable_display.set_cards(self.player.hand.cards)
        self.hand_display.set_cards(self.player.hand.cards)
        
    def render(self, s=screen):
        if(self.initialized == False):
            self.initialize()
            self.initialized = True
    
        playerTitle = futura48.render(f"{self.player.name}", True, (0,0,0))
        offsetblit(playerTitle, s, x=(WIDTH/2), y=(self.rel_height/2))
        instructions1 = futura32.render(f"Select a card to play.", True, (0,0,0))
        offsetblit(instructions1, s, x=(WIDTH/2), y=(self.rel_height/2)+40)
        instructions2 = futura32.render(f"Use arrow keys to select a card, then press enter", True, (0,0,0))
        offsetblit(instructions2, s, x=(WIDTH/2), y=(self.rel_height/2)+75)
        
        selectableTitle = futura32.render("Selectable Cards", True, (0,0,0))
        s.blit(selectableTitle, (0, (HEIGHT/2)-50))
        
        self.selectable_display.render(s=s)
        
        handTitle = futura32.render("Your hand:", True, (0,0,0))
        s.blit(handTitle, (0, 0))
        
        self.hand_display.render(s=s)
        
        leader = self.screen.game.players[findex(self.screen.screen.lead_player_index, self.screen.game.players)]
        leadMessage = f"{leader.name} lead"
        if(self.player.team == leader.team) and (self.player != leader):
            leadMessage = f"{leadMessage} (your teammate)."
        else:
            leadMessage = f"{leadMessage}."
            
        leadTitle = futura32.render(leadMessage, True, (0,0,0))
        s.blit(leadTitle, (WIDTH-leadTitle.get_width(), 0))
        
        teamScore = futura32.render(f"Your team currently has {self.game.round.trick_scores[self.player.team]} tricks.", True, (0,0,0))
        s.blit(teamScore, (WIDTH-teamScore.get_width(), self.rel_height-teamScore.get_height()))
        
    def event(self, e):
        self.selectable_display.event(e)
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_RETURN):
                # add the card to the trick pile
                selected_card = self.player.hand.cards[indexOf(self.selectable_display.cards[self.selectable_display.selected], self.player.hand.cards)]
                self.screen.trick.add_card(selected_card, self.player)
                self.player.hand.remove_card(selected_card)
                self.alive = False
                self.initialized= False
        
class TrickScreen(Flow):
    def __init__(self, screen):
        self.screen: RoundScreen = screen
        self.game: Game = self.screen.game
        self.alive = True
        self.result: Trick_result = None;
        self.trick_display = CardDisplay((0, 50))
        self.trick = None;
        self.initialized = False
        self.player_turn_i = 0;
        
        self.trick_turn_screen_active = True;
        self.trick_turn_screen = PlayerTrickSelectScreen(self)
    def reset(self):
        self.trick = Trick(self.game.round.trump, self.game.players, self.screen.lead_player_index)
        self.player_turn_i = 0;
        self.result = None
        self.alive = True
        self.trick_turn_screen_active = True
        self.trick_turn_screen.reset()
        

    def initialize(self):
        self.trick = Trick(self.game.round.trump, self.game.players, self.screen.lead_player_index)
        
    def check_end(self):
        if(self.player_turn_i > 3 and self.trick_turn_screen_active == True):
            # when the trick is done, call on the trick to get winner info
            self.result = self.trick.winner()
            self.alive = False 
            self.trick_turn_screen_active = False
            self.trick_turn_screen.alive = False
    
    def check_end_of_play(self):
        if(self.trick_turn_screen.alive == False and self.trick_turn_screen_active == True):
            self.player_turn_i += 1
            self.trick_turn_screen.alive = True   
            
    def render(self):
        if(self.initialized == False):
            self.initialize()
            self.initialized = True
        self.check_end()
        self.check_end_of_play()
        # self.check_end()
        
        if(self.alive == False):
            return
        screen.fill((255,255,255))
        ## top half is for trick pile
        # # bottom half (y>211) is for player specific
        handTitle = futura32.render("Trick pile:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        self.trick_display.set_cards(self.trick.cards)
        self.trick_display.render()
        
        handTitle = futura32.render(f"Trump is {format_suit(self.game.round.trump)}", True, (0,0,0))
        screen.blit(handTitle, (WIDTH-handTitle.get_width(), 0))
        
        # different layer for player turns
        trick_surf = pygame.surface.Surface((WIDTH, HEIGHT-211))
        trick_surf.fill((255,255,255))
        self.trick_turn_screen.render(s=trick_surf)
        screen.blit(trick_surf, (0,211))
    
    def event(self, e):
        self.trick_turn_screen.event(e)

class RoundScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.alive = True
        self.card_display = CardDisplay()
        self.trick_i = 0;
        # start initially with the player next to dealer
        self.lead_player_index = None;
        self.initialized = False
        
        self.trick_screen_active = False;
        self.trick_screen = TrickScreen(self);
        self.trick_screen.alive = False;
        pass
    def reset(self):
        self.__init__(self.game)
    def initialize(self):
        if(self.initialized == False):
            if(self.trick_screen.result == None):
                self.lead_player_index = self.game.round.dealer_index+1
                self.trick_i=0
                self.initialized=True
            else:
                self.trick_i = 0
                self.lead_player_index = indexOf(self.game.round.find_player_by_id(self.trick_screen.result.id), self.game.players)
                self.initialized = True
            self.trick_screen_active = True
            self.trick_screen.alive = True
            
    def trick(self):
        if(self.trick_screen_active == True and self.trick_screen.alive == True):
            self.trick_screen.render()
        if(self.trick_screen_active == True and self.trick_screen.alive == False):
            # receive information from the trick
            res: Trick_result = self.trick_screen.result
            winning_player:EuchrePlayer = self.game.round.find_player_by_id(res.id)
            winning_card = res.card
            winning_team = winning_player.team
            
            self.game.round.trick_scores[winning_team] += 1
            # every trick one gives an internal score to the corresponding team
            # increase trick by 1
            self.trick_i += 1
            self.lead_player_index = indexOf(winning_player, self.game.players)
            
            if(self.trick_i <= 4):
                #reactivate the new trick screen
                self.trick_screen.reset()
            else:
                # 5 cards have been played; round over
                self.trick_screen_active = False
                self.alive = False
            
    def render(self):
        self.initialize()
        self.trick()
        # if(self.trick_screen_active == False):
        #     self.alive = False

    def event(self, e):
        if(self.trick_screen_active == True):
            self.trick_screen.event(e)
            
class EndroundScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.points_given = False;
        self.alive = True
    def reset(self):
        self.__init__(self.game)    
    def render(self):
        screen.fill((255,255,255))
        
        res: RoundResult = self.game.round.get_score()

        if(self.points_given == False):
            self.game.scores[res.winning_team] += res.points
            self.points_given = True
            
        euchreTitle = futura48.render("Round over", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        winnerSubtitle = futura32.render(f"Team {res.winning_team} wins, gets {res.points} points.", True, (0,0,0))
        offsetblit(winnerSubtitle, screen, x=(WIDTH/2), y=(HEIGHT/2)+75)
        
        teamMessage = f"{self.game.round.caller.name} (on team {self.game.round.caller.team}) called trump"
        if(self.game.round.caller.team != res.winning_team):
            teamMessage = f"{teamMessage}, and their team was Euchred."
        else:
            teamMessage = f"{teamMessage}."
        
        teamSubtitle = futura32.render(teamMessage, True, (0,0,0))
        offsetblit(teamSubtitle, screen, x=(WIDTH/2), y=(HEIGHT/2)+115)
        # score info later
        playButton = futura64.render("Press Enter to continue", True, (0,50,255))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
        
        pass;
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.alive = False
                return
class EndgameScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.alive = True
        self.card_display = CardDisplay()
    
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura48.render("Game over.", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        
        playButton = futura64.render("Press Enter to continue", True, (0,50,255))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
        
        pass;
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.alive = False
                return


class Sequence:
    def __init__(self,screen_sequence):
        self.alive = False

        self.screen_index = 0;
        # array of Flows
        self.screen_sequence = screen_sequence
        self.view: Flow = None
        self.refresh_view()
    def reset(self):
        for sequence in self.screen_sequence:
            sequence.reset()
            self.__init__(self.screen_sequence)
    def start(self):
        self.alive = True
    def refresh_view(self):
        self.view = self.screen_sequence[self.screen_index]
    def event(self, e):
        self.view.event(e)
    def run(self):
        if(self.view.alive == False):
            if(self.screen_index+1 > (len(self.screen_sequence)-1)):
                self.alive = False
                return
            else:
                self.screen_index += 1
                self.refresh_view()
        self.view.render()
            

class GameScreen:
    def __init__(self):
        self.game = Game()
        # 0 is pregame only need once, 1 is round need as many times until win, 2 is endgame only need once
        self.sequence_active_index = 0;
        self.sequence: Sequence = None;
        self.pregame = Sequence([MainScreen(), PlayerSelectScreen(self.game), PregameScreen()])
        self.round = Sequence([PreroundScreen(self.game), RoundScreen(self.game), EndroundScreen(self.game)])
        self.endgame = Sequence([EndgameScreen(self.game)])
        self.sequences = [self.pregame, self.round, self.endgame]
        # loop round until game over
        # pregame: menu -> players -> splash
        # game: deal -> preround 1 up to x4 -> maybe preround 2 up to x4 -> trick round x4 -> postround score page
        # postgame: winning teams
        self.refresh_sequence()
    def refresh_round(self):
        self.game.round = None;
        self.round = Sequence([PreroundScreen(self.game), RoundScreen(self.game), EndroundScreen(self.game)]);
        
    def refresh_sequence(self):
        self.sequence = self.sequences[self.sequence_active_index]
        self.sequence.alive = True
    def end_of_sequence(self):
        if(self.sequence_active_index+1 > (len(self.sequences)-1)):
            return True
        else:
            return False
    def start(self):
        running = True
        while running:
            if(self.sequence.alive == False):
                # new sequence
                if(self.sequence_active_index == 1):
                    # a round just ended
                    # if the score is less than 10 on either team, continue the game
                    wincheck = self.game.check_win()
                    if(wincheck[0] == False):
                        # nobody has won yet, so reset the round
                        # relinquish cards
                        self.game.round.postround();
                        self.game.round = None     
                                           
                        self.game.dealer_index+=1
                        self.sequence.reset()
                        self.refresh_sequence()
                    elif(wincheck[0] == True):
                        #a team has won
                        if not self.end_of_sequence():
                            self.sequence_active_index += 1
                else:
                    if not self.end_of_sequence():
                        self.sequence_active_index += 1
                    else:
                        running = False;
                self.refresh_sequence();    
                    
            for event in pygame.event.get():
                # pass events to the sequence
                self.sequence.event(event)
                # close the window when press close
                if event.type == pygame.QUIT:
                    running = False
            # render whichever sequence is currently running
            self.sequence.run()
            pygame.display.flip()
            clock.tick(75)
        else:
            pygame.quit()
GameScreen().start()