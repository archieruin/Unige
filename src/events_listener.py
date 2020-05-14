import pygame
from pygame.constants import *

from src.entities.crosshair import Crosshair
from src.entities.player import Player


class EventsListener(object):

    def __init__(self, game):
        self.__screen_width = game.screen_width
        self.__screen_height = game.screen_height
        self.__player: Player = game.player
        self.__crosshair: Crosshair = game.crosshair

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        self.__update_player_moving(keys)
        self.__update_player_watching()

    def __update_player_watching(self):
        mouse_x = self.__crosshair.get_center()[0]
        player_x = self.__player.get_center()[0]

        if mouse_x > player_x:
            self.__player.watch_right = True
            self.__player.watch_left = False
        if mouse_x < player_x:
            self.__player.watch_left = True
            self.__player.watch_right = False

    def __update_player_moving(self, keys):
        player_x = self.__player.get_pos()[0]
        player_y = self.__player.get_pos()[1]
        player_width = self.__player.get_width()
        player_height = self.__player.get_height()

        if keys[K_w]:
            self.__player.move_top = True
            self.__player.move_down = False
            self.__player.idle = False
        elif keys[K_s]:
            self.__player.move_down = True
            self.__player.move_top = False
        else:
            self.__player.idle = True
            self.__player.move_down = False
            self.__player.move_top = False

        if keys[K_a]:
            self.__player.move_left = True
            self.__player.move_right = False
            self.__player.idle = False
        elif keys[K_d]:
            self.__player.move_right = True
            self.__player.move_left = False
            self.__player.idle = False
        else:
            self.__player.idle = True
            self.__player.move_right = False
            self.__player.move_left = False
