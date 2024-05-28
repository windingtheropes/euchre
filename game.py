# euchre executable game by Jack Anderson
from libeuchre import Game
# import pygame
from libeuchre import EuchreCard
from libcards import Deck


g = Game()
g.config_players()
g.start()
