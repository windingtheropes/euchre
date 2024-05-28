# graphics for the game :) by jack anderson
import pygame
pygame.init()


screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

while True:
    pygame.display.flip()
    clock.tick(60)