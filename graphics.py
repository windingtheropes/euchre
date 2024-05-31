# graphics for the game :) by jack anderson
# plan

# class which holds a method which calls events
# a render function
# therefore it can handle its own input and updates for as long as it exists
# the running function should have an activescreen method
# class for screens will have an exit code, 0 will continue rendering it, 1 will stop rendering it, and another screen should be provided

import pygame
from typing import Callable
pygame.init()

WIDTH = 1536
HEIGHT = 864
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Euchre")
from libeuchre import EuchreCard
from libcards import Jack, Queen, King, Ace, Clubs, Diamonds, Spades, Hearts

img = pygame.image.load("img/jack_of_hearts.png").convert()
# dimensions of any given card is 222x323, so this is half scale
img = pygame.transform.scale(img, (222/2,323/2))
def font(font, size):
    return pygame.font.SysFont(font, size)

class Button:
    def __init__(self):
        self.button = pygame.draw.rect(screen, pygame.Color(0,0,0), pygame.Rect(50,50,50,50))
        self.is_click = False
        
    def is_hover(self):
        mx, my = pygame.mouse.get_pos()
        if((my <= self.button.bottom) and (my >= self.button.top)) and ((mx >= self.button.left) and (mx <= self.button.right)):
            return True
        return False
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(self.is_hover()):
                self.is_click = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_click = False
            
    # these functions should be re-implemented as a child class
    def render(self):
        if(self.is_hover()):
            self.button = pygame.draw.rect(screen, pygame.Color(0,0,255), pygame.Rect(50,50,50,50))
        if(self.is_click):
            self.button = pygame.draw.rect(screen, pygame.Color(0,255,0), pygame.Rect(50,50,50,50))            
        else:
            self.button = pygame.draw.rect(screen, pygame.Color(0,0,0), pygame.Rect(50,50,50,50))

class Textbox:
    def __init__(self, locx, locy):
        self.tb = font("Futura", 32).render(f"|", True, (255,255,255))
        self.locx = locx
        self.locy = locy
        self.posx = 0 #100
        self.posy = 0 #100
        self.wid = 300
        self.hei = 50
        self.surf = pygame.surface.Surface((self.wid, self.hei))
        self.charlim = 16
        self.button = pygame.draw.rect(self.surf, pygame.Color(0,0,0), pygame.Rect(self.posx,self.posy,self.wid,self.hei))
        self.is_click = False
        self.toggle  = False
        self.text = ""
        
    def is_hover(self):
        mx, my = pygame.mouse.get_pos()
        # get relative position by subtract the expected locy and locx on screen, given at creation
        if((my-self.locy <= self.button.bottom) and (my-self.locy >= self.button.top)) and ((mx-self.locx >= self.button.left) and (mx-self.locx <= self.button.right)):
            return True
        return False
    
    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if(self.is_hover()):
                self.is_click = True
                self.toggle = not self.toggle
        if event.type == pygame.KEYUP:
            if(self.toggle == True):
                if(len(self.text) < self.charlim):
                    if(event.key == pygame.K_a):
                        self.text = f"{self.text}a"
                    elif(event.key == pygame.K_b):
                        self.text = f"{self.text}b"
                    elif(event.key == pygame.K_c):
                        self.text = f"{self.text}c"
                    elif(event.key == pygame.K_d):
                        self.text = f"{self.text}d"
                    elif(event.key == pygame.K_e):
                        self.text = f"{self.text}e"
                    elif(event.key == pygame.K_f):
                        self.text = f"{self.text}f"
                    elif(event.key == pygame.K_g):
                        self.text = f"{self.text}g"
                    elif(event.key == pygame.K_h):
                        self.text = f"{self.text}h"
                    elif(event.key == pygame.K_i):
                        self.text = f"{self.text}i"
                    elif(event.key == pygame.K_j):
                        self.text = f"{self.text}j"
                    elif(event.key == pygame.K_k):
                        self.text = f"{self.text}k"
                    elif(event.key == pygame.K_l):
                        self.text = f"{self.text}l"
                    elif(event.key == pygame.K_m):
                        self.text = f"{self.text}m"
                    elif(event.key == pygame.K_n):
                        self.text = f"{self.text}n"
                    elif(event.key == pygame.K_o):
                        self.text = f"{self.text}o"
                    elif(event.key == pygame.K_p):
                        self.text = f"{self.text}p"
                    elif(event.key == pygame.K_q):
                        self.text = f"{self.text}q"
                    elif(event.key == pygame.K_r):
                        self.text = f"{self.text}r"
                    elif(event.key == pygame.K_s):
                        self.text = f"{self.text}s"
                    elif(event.key == pygame.K_t):
                        self.text = f"{self.text}t"
                    elif(event.key == pygame.K_u):
                        self.text = f"{self.text}u"
                    elif(event.key == pygame.K_v):
                        self.text = f"{self.text}v"
                    elif(event.key == pygame.K_w):
                        self.text = f"{self.text}w"
                    elif(event.key == pygame.K_x):
                        self.text = f"{self.text}x"
                    elif(event.key == pygame.K_y):
                        self.text = f"{self.text}y"
                    elif(event.key == pygame.K_z):
                        self.text = f"{self.text}z"
                    elif(event.key == pygame.K_SPACE):
                        self.text = f"{self.text} "
                if(event.key == pygame.K_BACKSPACE):
                    self.text = self.text[:-1]
            
    # these functions should be re-implemented as a child class
    def render(self):
        # layer
        # surf = pygame.surface.Surface((WIDTH, HEIGHT))
        text = font("Futura", 32).render(f"{self.text.upper()}|", True, (255,255,255))
        
        if(self.is_hover()):
            self.button = pygame.draw.rect(self.surf, pygame.Color(10,10,50), pygame.Rect(self.posx,self.posx,self.wid,self.hei))
        if(self.toggle):
            self.button = pygame.draw.rect(self.surf, pygame.Color(0,0,100), pygame.Rect(self.posx,self.posx,self.wid,self.hei))          
        else:
            self.button = pygame.draw.rect(self.surf, pygame.Color(0,0,0), pygame.Rect(self.posx,self.posx,self.wid,self.hei))
        self.surf.blit(text, (self.posx,self.posy))
        return self.surf



class Flow:
    def __init__(self):
        pass;
def menu():
    screen.fill((255,255,255))
class CardDisplay:
    def __init__(self):
        self.cards = []
        self.card_imgs = []
        pass;
    def load(self):
        for card in self.cards:
            c = pygame.image.load(f"img/{card.format().lower().replace(' ', '_')}.png")
            # dimensions of any given card is 222x323, so this is half scale
            c = pygame.transform.scale(c, (222/2,323/2))
            self.card_imgs.append(c)
    def render(self):
        i = 0
        for cimg in self.card_imgs:
            screen.blit(cimg, (i,0))
            i+=222/2
    def set_cards(self, cards):
        self.cards = cards
        self.card_imgs = []
        self.load()
        
class GameScreen:
    def __init__(self):
        view: Flow = None;
        pass
    def start(self):
        # b = Button()
        t = Textbox(100,50)
        # c = CardDisplay()
        
        running = True
        while running:
            for event in pygame.event.get():
                t.on_event(event)
                # b.on_event(event)
                # close window if pressed close
                if event.type == pygame.QUIT:
                    running = False
            menu()
        # screen.blit(img, (50,0))
            # b.render()
            screen.blit(t.render(), (100,50))
            # c.set_cards([EuchreCard(King,Hearts), EuchreCard(10, Clubs), EuchreCard(9, Spades), EuchreCard(Jack, Clubs)])
            # c.render()
            pygame.display.flip()
            clock.tick(60)
        else:
            pygame.quit()
GameScreen().start()
