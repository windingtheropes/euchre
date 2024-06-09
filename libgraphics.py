import pygame
from helpers import flip, findex, indexOf
from libeuchre import Game, EuchrePlayer, Round, Trick, Trick_result

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

class Button:
    def __init__(self, obj, coords=(0,0)):
        self.obj = obj
        self.rect = obj.get_rect()
        self.x, self.y = coords
        self.is_click = False
        
    def is_hover(self):
        ty, lx = self.rect.topleft
        by, rx = self.rect.bottomright
        
        mx, my = pygame.mouse.get_pos()
        
        if(ty+self.y <= my and my <= by+self.y) and (lx+self.x <= mx and mx <= rx+self.x):
            return True
        return False
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(self.is_hover() == True):
                self.is_click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_click = False
                            
    # these functions should be re-implemented as a child class
    def render(self):
        screen.blit(self.obj, (self.x, self.y))

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
            
    def render(self):
        # for e in pygame.event.get(): self.event(e)
        x = self.x
        # print(self.selected)
        for i in range(0, len(self.card_imgs)):
            cimg = self.card_imgs[i]
            screen.blit(cimg, (x,self.y))
            x+=self.width/2
        if(self.selectable == True):
            # indicate selected card by a red line under it
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.x+(self.selected*(222/2)),self.y+(323/2),(222/2),10))
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
        self.load()
   
class Flow:
    def __init__(self):
        self.alive = True
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
                    print(f"player {self.player} added")
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
        self.player = self.game.players[findex(self.screen.player_rot_i, self.game.players)]
        self.choices_display.set_cards(self.game.round.callable_suits(as_cards=True))
        self.hand_display.set_cards(self.player.hand.cards)
        
    def render(self):
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
                print("herer")
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
        self.dealer_rot_i = 0;
        
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
        
    def init__round(self):
        # initialize the round, deck
        if self.round_initialized == False:
            self.game.round = Round(self.game.deck, self.game.players, findex(self.dealer_rot_i, self.game.players))
            self.game.deck.shuffle()
            self.game.round.deal()
            self.dealer_rot_i += 1;
            print(self.game.players[self.dealer_rot_i].name)
            
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
                    print(self.game.players[self.player_rot_i].name)
                    self.preround2_active = True
                self.pickupround_active = False   
        if(self.game.round.called_on_round == 1):
            self.pickup_active = True
    def pickup(self):
        if(self.pickup_screen.alive == False):
            self.pickup_active = False;
        if(self.pickup_active == True):
            self.pickup_screen.render()   

    def preround2(self):
        if(self.game.round.called_on_round == 2):
            self.preround2_active = False
            # self.select_trump_active = True
        if(self.preround2_active == True):
            self.preround2_screen.render()
        if(self.preround2_screen.alive == False and self.preround2_active == True):
            player = self.game.players[findex(self.player_rot_i, self.game.players)]    
            # player is not dealer, not on 4th player so not the dealer
            if(player.id != self.game.round.dealer.id) and self.preround2_i < 3:
                if(self.pickupround_screen.result == 1):
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
        print(self.select_trump_active)
        if(self.select_trump_active == True):
            self.select_trump_screen.render()
        if(self.select_trump_screen.alive == False):
            self.select_trump_active = False
            print(f"trump is {self.game.round.trump}")   
    
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

class PlayerTrickSelectScreen(Flow):
    def __init__(self, screen):
        self.screen: TrickScreen = screen
        self.game: Game = self.screen.game
        self.alive = True
        self.result = None;
        self.player: EuchrePlayer = None;
        self.hand_display = CardDisplay((0,50+250), selectable=True)
        self.selectable_display = CardDisplay((0, 250+200))
        # 1 is call 0 is pass
        self.initialized = False
        
    def initialize(self):
        self.player = self.game.round.dealer
        # leader can play any card
        if(self.screen.player_turn_i == 0):
            self.selectable_display.set_cards(self.player.hand.cards)
        else:
            lead_card = self.screen.trick.cards[0]
            cards_of_suit = self.player.hand.find_suit(lead_card.suit)
            # must follow suit if suit is found otherwise any card
            if(len(cards_of_suit) > 0):
                self.selectable_display.set_cards(cards_of_suit)
            else:
                self.selectable_display.set_cards(self.player.hand.cards)
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
        self.selectable_display.event(e)
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_RETURN):
                # add the card to the trick pile
                self.screen.trick.add_card(self.player.hand.cards[self.selectable_display.selected], self.player)
                self.alive = False
        
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
        
    def initialize(self):
        self.trick = Trick(self.game.round.trump, self.game.players, self.screen.lead_player_index)
        
    def check_end(self):
        if(self.player_turn_i > 3):
            # when the trick is done, call on the trick to get winner info
            self.result = self.trick.winner()
            self.alive = False
        
    def render(self):
        if(self.initialized == False):
            self.initialize()
            self.initialized = True
    
        
        ## top half is for trick pile
        # bottom half (y>211) is for player specific
        handTitle = futura32.render("Trick pile:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        self.trick_display.set_cards(self.trick.cards)
        self.trick_display.render()
        
        self.trick_turn_screen.render()
        
        self.check_end()
        
    def event(self, e):
        self.trick_turn_screen.event(e)
             

class RoundScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.alive = True
        self.card_display = CardDisplay()
        self.trick_i = 0;
        # start initially with the player next to dealer
        self.lead_player_index = self.game.round.dealer_index+1
        self.initialized = False
        
        self.trick_screen_active = True;
        self.trick_screen = TrickScreen(self);
        pass
    def initialize(self):
        if(self.initialized == False):
            self.trick_i=0
            self.initialized=True
            
    def trick(self):
        if(self.trick_screen_active == True):
            self.trick_screen.render()
        if(self.trick_screen_active == True and self.trick_screen.alive == False):
            # receive information from the trick
            # winning card
            # winning player
            # trcikresult class
            res: Trick_result = self.trick_screen.result
            winning_player = self.game.round.find_player_by_id(res.id)
            winning_card = res.card
            
            # once a player wins, they go next
            # trick ended
            # do stuff
            # 5 cards in a hand so 5 tricks
            # 4 is 5
            if(self.trick_i < 5):
                # within bounds of trick round
                self.lead_player_index = indexOf(winning_player, self.game.players)
                self.trick_i += 1
                #reactivate the new trick screen
                self.trick_screen.alive = True
                # need to reset its state
            else:
                self.trick_screen_active = False
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
        self.alive = True
        self.card_display = CardDisplay()
        
        pass
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura48.render("Euchre Preround", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        
        playButton = futura64.render("Press Enter to continue", True, (0,50,255))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
        
        pass;
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                print("preround 1 exit")
                self.alive = False
                return
class EndgameScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.alive = True
        self.card_display = CardDisplay()
        
        pass
    def render(self):
        screen.fill((255,255,255))
        
        euchreTitle = futura48.render("Euchre Preround", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        
        playButton = futura64.render("Press Enter to continue", True, (0,50,255))
        offsetblit(playButton, screen, x=(WIDTH/2), y=(HEIGHT/2)+250)
        
        
        pass;
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                print("preround 1 exit")
                self.alive = False
                return


class GameScreen:
    def __init__(self):
        self.game = Game()
        self.sequence = 0;
        self.si = 0;
        self.end_of_sequence = False
        self.sequences = [[MainScreen(), PlayerSelectScreen(self.game), PregameScreen()], [PreroundScreen(self.game), RoundScreen(self.game), EndroundScreen(self.game)], [EndgameScreen(self.game)]]
        # pregame: menu -> players -> splash
        # game: deal -> preround 1 up to x4 -> maybe preround 2 up to x4 -> trick round x4 -> postround score page
        # postgame: winning teams
        self.view: Flow = self.sequences[self.sequence][self.si];
        pass
    def start(self):
        running = True
        while running:
            # progress to next screen in sequence
            if(self.view.alive == False):
                if(self.si > len(self.sequences[self.sequence])-1): 
                    self.end_of_sequence = True
                    print("end of sequence")
                else:
                    self.end_of_sequence = False
                    self.view = self.sequences[self.sequence][self.si]
                self.si += 1;
            # progress to the next set of screens (new sequence)
            if(self.end_of_sequence == True):
                self.si = 0;
                self.sequence += 1;
                self.end_of_sequence = False
                if(self.sequence > len(self.sequences)-1):
                    print("no more sequences")
                
                    
            for event in pygame.event.get():
                # close window if pressed close
                self.view.event(event)
                if event.type == pygame.QUIT:
                    running = False
            self.view.render()
            pygame.display.flip()
            clock.tick(75)
        else:
            pygame.quit()
GameScreen().start()