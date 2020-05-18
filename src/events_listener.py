import pygame
from pygame.constants import *

from src import settings
from src.entities.crosshair import Crosshair
from src.entities.player import Player


class EventsListener(object):

    def __init__(self, player):
        self.__screen_width = settings.SCREEN_WIDTH
        self.__screen_height = settings.SCREEN_HEIGHT
        self.__player: Player = player
        self.__crosshair: Crosshair = settings.crosshair

    def update(self):

        keys = pygame.key.get_pressed()
        self.__update_player_moving(keys)
        self.__update_player_watching()
