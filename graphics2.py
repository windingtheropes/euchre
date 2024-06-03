import pygame

pygame.init()

WIDTH = 1536
HEIGHT = 864
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Euchre")

class Flow:
    def __init__(self):
        self.alive = True
        pass
    def render(self):
        pass
    def event(self, e):
        pass;

class MainScreen(Flow):
    def __init__(self):
        self.alive = True
        pass
    def render(self):
        screen.fill((255,255,255))
        
        pass;
    def event(self, e):
        pass;

class GameScreen:
    def __init__(self):
        self.view: Flow = MainScreen();
        pass
    def start(self):
        running = True
        while running:
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