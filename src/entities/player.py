import pygame

from .entity import Entity
from .. import settings


class Player(Entity):
    
    def __init__(self, x, y, width, height, speed=5, player_res=None):
        super().__init__(x, y, width, height)
        self.__speed = speed
        self.__player_res = settings.player_res

        self.watch_left = False
        self.watch_right = True

        self.move_top = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.idle = True

        self.__idle_anim = [
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f0.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f1.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f2.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f3.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f4.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f5.png')), width, height)
        ]

        self.__move_anim = [
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f0.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f1.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f2.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f3.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f4.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f5.png')), width, height)
        ]

        self.__anim = self.__idle_anim
        self.__frame = 0
        self.__image = self.__anim[int(self.__frame)]

    def update(self):
        self.__frame += 0.2
        if self.__frame >= len(self.__anim):
            self.__frame = 0

        self.__move()
        self.__watch()

        if not self.move_top and not self.move_down and not self.move_left and not self.move_right:
            self.__anim = self.__idle_anim
        else:
            self.__anim = self.__move_anim

    def draw(self, screen):
        screen.blit(self.__image, (self.get_center()[0], self.get_center()[1]))

    def handle_events(self, crosshair):
        keys = pygame.key.get_pressed()
        self.__update_player_watching(crosshair)
        self.__update_player_moving(keys)

    def __update_player_watching(self, crosshair):
        mouse_x = crosshair.get_center()[0]
        player_x = self.get_center()[0]

        if mouse_x > player_x:
            self.watch_right = True
            self.watch_left = False
        if mouse_x < player_x:
            self.watch_left = True
            self.watch_right = False

    def __update_player_moving(self, keys):
        player_x = self.get_pos()[0]
        player_y = self.get_pos()[1]
        player_width = self.get_width()
        player_height = self.get_height()

        if keys[pygame.K_w]:
            self.move_top = True
            self.move_down = False
            self.idle = False
        elif keys[pygame.K_s]:
            self.move_down = True
            self.move_top = False
        else:
            self.idle = True
            self.move_down = False
            self.move_top = False

        if keys[pygame.K_a]:
            self.move_left = True
            self.move_right = False
            self.idle = False
        elif keys[pygame.K_d]:
            self.move_right = True
            self.move_left = False
            self.idle = False
        else:
            self.idle = True
            self.move_right = False
            self.move_left = False

    def __watch(self):
        if self.watch_left:
            self.__image = self.h_flip(self.__anim[int(self.__frame)])
        else:
            self.__image = self.__anim[int(self.__frame)]

    def __move(self):
        if self.move_top:
            self._y -= self.__speed

        elif self.move_down:
            self._y += self.__speed

        if self.move_left:
            self._x -= self.__speed

        elif self.move_right:
            self._x += self.__speed
