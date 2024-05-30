# graphics for the game :) by jack anderson
import pygame
pygame.init()


screen = pygame.display.set_mode((1536,864))
clock = pygame.time.Clock()
pygame.display.set_caption("Euchre")



img = pygame.image.load("img/jack_of_hearts.png").convert()
# dimensions of any given card is 222x323, so this is half scale
img = pygame.transform.scale(img, (222/2,323/2))
running = True
while running:
    # the active screen could be a class, which has bindings to events, and has a render method.
     # activeScreen = 
    for event in pygame.event.get():
        # close window if pressed close
        if event.type == pygame.QUIT:
            running = False
        
    screen.blit(img, (50,0))
    pygame.display.flip()
    clock.tick(60)
else:
    pygame.quit()