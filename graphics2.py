import pygame
from helpers import flip
from libeuchre import Game, EuchrePlayer

pygame.init()

WIDTH = 1536
HEIGHT = 864
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Euchre")

def font(font, size):
    return pygame.font.SysFont(font, size)
futura128 = font("Futura", 128)
futura64 = font("Futura", 64)
futura48 = font("Futura", 48)

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
                if(self.player +1 <= 4):
                    controlled = self.selectedButton == 1
                    self.game.add_player(EuchrePlayer(name=f"Player {self.player}",controlled=controlled))
                    self.player+=1
                else:
                    self.alive = False
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                self.selectedButton = flip(self.selectedButton)

class GameScreen:
    def __init__(self):
        self.game = Game()
        self.sequence = [MainScreen(), PlayerSelectScreen(self.game)]
        self.vi = 0;
        self.view: Flow = self.sequence[self.vi];
        pass
    def start(self):
        running = True
        while running:
            # progress to next screen in sequence
            if(self.view.alive == False):
                self.vi += 1;
                if(self.vi > len(self.sequence)-1): 
                    for i in self.game.players:
                        print(f"{i.name} {i.controlled}")
                    print("Sequence fulfilled.")
                else:
                    self.view = self.sequence[self.vi]
                
            for event in pygame.event.get():
                # close window if pressed close
                self.view.event(event)
                if event.type == pygame.QUIT:
                    running = False
            self.view.render()
            pygame.display.flip()
            clock.tick(60)
        else:
            pygame.quit()
GameScreen().start()