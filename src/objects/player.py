import pygame

from .game_object import GameObject


class Player(GameObject):
    
    def __init__(self, x, y, width, height, speed=5, player_res=None):
        super().__init__(x, y, width, height, speed)
        self.__player_res = player_res

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

        self.__current_anim = self.__idle_anim
        self.__current_frame = 0
        self.__image = self.__current_anim[int(self.__current_frame)]

    def update(self):
        self.__current_frame += 0.2
        if self.__current_frame >= len(self.__current_anim):
            self.__current_frame = 0

        if self.move_top:
            self._y -= self._speed

        elif self.move_down:
            self._y += self._speed

        if self.move_left:
            self._x -= self._speed

        elif self.move_right:
            self._x += self._speed

        if not self.move_top and not self.move_down and not self.move_left and not self.move_right:
            self.__current_anim = self.__idle_anim
        else:
            self.__current_anim = self.__move_anim

        if self.watch_left:
            self.__image = self.h_flip(self.__current_anim[int(self.__current_frame)])
        else:
            self.__image = self.__current_anim[int(self.__current_frame)]

    def draw(self, screen):
        screen.blit(self.__image, (self.get_center()[0], self.get_center()[1]))
