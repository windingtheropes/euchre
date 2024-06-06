import pygame
from helpers import flip, findex
from libeuchre import Game, EuchrePlayer, Round

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
    def __init__(self, coords=(0,0)):
        self.cards = []
        self.x, self.y = coords
        self.width = 222;
        self.height = 323;
        self.card_imgs = []
    def load(self):
        for card in self.cards:
            c = pygame.image.load(f"img/{card.format().lower().replace(' ', '_')}.png")
            # dimensions of any given card is 222x323, so this is half scale
            c = pygame.transform.scale(c, (self.width/2,self.height/2))
            self.card_imgs.append(c)
            
    def render(self):
        for e in pygame.event.get(): self.event(e)
        x = self.x
        for cimg in self.card_imgs:
            screen.blit(cimg, (x,self.y))
            x+=self.width/2
    def event(self, e):
        pass
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
                print("Pregame exit")
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
    def render(self):
        
        euchreTitle = futura48.render(f"Player {self.screen.game.players[findex(self.screen.player_rot_i, self.screen.game.players)].name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions = futura32.render(f"Use arrow keys to select, then press enter", True, (0,0,0))
        offsetblit(instructions, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        
        kittyTitle = futura32.render("Kitty", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        kd = CardDisplay((0, HEIGHT/2))
        kd.set_cards([self.screen.game.round.kitty.cards[0]])
        kd.render()
        
        handTitle = futura32.render("Your hand:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        c = CardDisplay((0,50))
        print(findex(self.screen.player_rot_i, self.screen.game.players))
        c.set_cards(self.screen.game.players[findex(self.screen.player_rot_i, self.screen.game.players)].hand.cards)
        c.render()
        
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
                print("hey")
                if self.selectedButton == 0:
                    self.alive = False
                    self.result = 0
                elif self.selectedButton == 1:
                    self.alive = False;
                    self.result = 1
       
class Preround1Screen(Flow):
    def __init__(self, screen):
        self.screen = screen
        self.alive = True
        self.result = None;
        # 1 is call 0 is pass
        self.selectedButton = 0;
    def render(self):
        player = self.screen.game.players[findex(self.screen.player_rot_i, self.screen.game.players)]
        
        euchreTitle = futura48.render(f"Player {player.name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions = futura32.render(f"Use arrow keys to select, then press enter", True, (0,0,0))
        offsetblit(instructions, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        
        kittyTitle = futura32.render("Kitty", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        kd = CardDisplay((0, HEIGHT/2))
        kd.set_cards([self.screen.game.round.kitty.cards[0]])
        kd.render()
        
        handTitle = futura32.render("Your hand:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        c = CardDisplay((0,50))
        c.set_cards(player.hand.cards)
        c.render()
        
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
        self.alive = True
        self.result = None;
        
        # 1 is call 0 is pass
        self.selectedButton = 0;
    def render(self):
        player = self.screen.game.round.dealer
        euchreTitle = futura48.render(f"{player.name}", True, (0,0,0))
        offsetblit(euchreTitle, screen, x=(WIDTH/2), y=(HEIGHT/2))
        instructions1 = futura32.render(f"Picking up {self.screen.game.round.kitty.cards[0].format()}. Must discard a card.", True, (0,0,0))
        offsetblit(instructions1, screen, x=(WIDTH/2), y=(HEIGHT/2)+50)
        instructions2 = futura32.render(f"Use arrow keys to select a discard, then press enter", True, (0,0,0))
        offsetblit(instructions2, screen, x=(WIDTH/2), y=(HEIGHT/2)+100)
        
        kittyTitle = futura32.render("Kitty", True, (0,0,0))
        screen.blit(kittyTitle, (0, (HEIGHT/2)-50))
        
        kd = CardDisplay((0, HEIGHT/2))
        kd.set_cards([self.screen.game.round.kitty.cards[0]])
        kd.render()
        
        handTitle = futura32.render("Your hand:", True, (0,0,0))
        screen.blit(handTitle, (0, 0))
        
        c = CardDisplay((0,50))
        c.set_cards(player.hand.cards)
        c.render()
        
        handTitle = futura32.render(f"{self.screen.game.round.dealer.name} dealt.", True, (0,0,0))
        screen.blit(handTitle, (WIDTH-handTitle.get_width(), 0))
        
        
    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                pass
            if e.key == pygame.K_RETURN:
                pass
      
          
class Preround2Screen(Flow):
    def __init__(self, screen):
        self.screen = screen
        
class PreroundScreen(Flow):
    def __init__(self, game):
        self.game: Game = game;
        self.alive = True
        self.card_display = CardDisplay()
        
        # meta round
        self.round_init = True
        self.dealer_rot_i = 0;
        
        # round
        self.player_rot_i = self.dealer_rot_i+1;
        
        # pickup call round
        self.pickupround_active = True
        self.preround1_i = 0;
        self.pickupround_screen = Preround1Screen(self)
        
        # dealer pickup?
        self.pickup_active = False
        self.pickup_screen = PickupScreen(self)
        # we don't actually need to know what card the player discarded
        
        
    def init__round(self):
        if self.round_init == True:
            self.game.round = Round(self.game.deck, self.game.players, findex(self.dealer_rot_i, self.game.players))
            self.game.deck.shuffle()
            self.game.round.deal()
            self.dealer_rot_i += 1;
            
        self.round_init = False
    
    def preround1(self):
        if(self.pickupround_active == True):
            self.pickupround_screen.render() 
        if(self.pickupround_screen.alive == False):
            player = self.game.players[findex(self.player_rot_i, self.game.players)]    
            if(player.id != self.game.round.dealer.id) and self.preround1_i < 3:
                if(self.pickupround_screen.result == 1):
                    # a player calls
                    self.game.round.pr1_call(player, False)
                else:
                    # a player passes
                    pass
                self.preround1_i += 1
                self.player_rot_i += 1
                self.pickupround_screen.alive = True
            elif(player.id == self.game.round.dealer.id) and self.preround1_i == 3:
                if(self.pickupround_screen.result == 1):
                    # dealer calls to pick up
                    self.game.round.pr1_call(player, False)
                else:
                    # dealer passes and preround 2 is needed
                    pass
                self.pickupround_active = False   
        if(self.game.round.called_on_round == 1):
            self.pickup_active = True
    def pickup(self):
        if(self.pickup_active == True):
            self.pickup_screen.render()        
    def render(self):
        self.init__round()
        screen.fill((255,255,255))
        
        
        self.preround1()
        self.pickup()   
        # self.preround2() 

        
        
    def event(self,e):
        if(self.pickupround_screen.alive == True):
            self.pickupround_screen.event(e)
    # def event(self, e):
    #     if e.type == pygame.KEYDOWN:
    #         if e.key == pygame.K_RETURN:
    #             print("preround 1 exit")
    #             self.alive = False
    #             return
  

class RoundScreen(Flow):
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
            clock.tick(24)
        else:
            pygame.quit()
GameScreen().start()