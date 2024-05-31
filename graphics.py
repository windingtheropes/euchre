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
        self.load()
        
class GameScreen:
    def __init__(self):
        view: Flow = None;
        pass
    def start(self):
        # b = Button()
        c = CardDisplay()
        
        running = True
        while running:
            for event in pygame.event.get():
                # b.on_event(event)
                # close window if pressed close
                if event.type == pygame.QUIT:
                    running = False
            menu()
        # screen.blit(img, (50,0))
            # b.render()
            c.render()
            c.set_cards([EuchreCard(14,2), EuchreCard(13,2),EuchreCard(12,2),EuchreCard(11,2),EuchreCard(10,3)])
            pygame.display.flip()
            clock.tick(60)
        else:
            pygame.quit()
GameScreen().start()
