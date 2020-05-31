import random
from math import sqrt

import pygame
from pygame.sprite import Sprite

from game import settings
from game.entities.entity import Entity


class Slime(Entity, Sprite):

    def __init__(self, x, y, width, height, speed=3, health=5):
        super().__init__(x, y, width, height)
        Sprite.__init__(self)

        self.__slime_res = settings.slime_res
        self.__speed = speed
        self.__max_vel = speed * 5
        self.__health = health
        self.__hit_countdown = 0
        self.__last_damage_ticks = 0

        self.__move_anim = [
            self.scale(self.load(str(self.__slime_res / 'slime_run_anim_f0.png')), width, height),
            self.scale(self.load(str(self.__slime_res / 'slime_run_anim_f1.png')), width, height),
            self.scale(self.load(str(self.__slime_res / 'slime_run_anim_f2.png')), width, height),
            self.scale(self.load(str(self.__slime_res / 'slime_run_anim_f3.png')), width, height),
            self.scale(self.load(str(self.__slime_res / 'slime_run_anim_f4.png')), width, height),
            self.scale(self.load(str(self.__slime_res / 'slime_run_anim_f5.png')), width, height)
        ]

        self.__anim = self.__move_anim
        self.__frame = 0
        self.image = self.__anim[int(self.__frame)]
        self.rect = self.image.get_rect(topleft=self.get_pos())

    def draw(self, screen):
        screen.blit(self.image, (self._x, self._y))
        pygame.draw.rect(screen, (0, 200, 0), self.rect)

    def update(self, dt):
        self._x += self._vx
        self._y += self._vy

        self.__frame += 0.2
        if self.__frame >= len(self.__anim):
            self.__frame = 0
        self.image = self.__anim[int(self.__frame)]
        self.rect = self.image.get_rect(topleft=self.get_pos())

        if self.__health <= 0:
            self.kill()

    def move_to_player(self, player_pos):
        self_pos = self.get_pos()
        dir_x = self_pos[0] - player_pos[0]
        dir_y = self_pos[1] - player_pos[1]
        dir_len = sqrt(pow(dir_x, 2) + pow(dir_y, 2))
        dir_x = dir_x / dir_len
        dir_y = dir_y / dir_len
        self._vx = -dir_x * self.__speed
        self._vy = -dir_y * self.__speed

    def throw(self, from_pos, force):
        self_pos = self.get_pos()
        dir_x = self_pos[0] - from_pos[0]
        dir_y = self_pos[1] - from_pos[1]
        dir_len = sqrt(pow(dir_x, 2) + pow(dir_y, 2))
        if dir_x or dir_y:
            dir_x = dir_x / dir_len
            dir_y = dir_y / dir_len
        self._vx += dir_x * force
        self._vy += dir_y * force

    def take_damage(self, from_pos, damage):
        seconds_passed = (pygame.time.get_ticks() - self.__last_damage_ticks) / 1000
        if seconds_passed > 0.1:
            self.__health -= damage
            self.__last_damage_ticks = pygame.time.get_ticks()
        self.__hit_countdown = 5
        pos = self.get_pos()
        dir_x = pos[0] - from_pos[0]
        dir_y = pos[1] - from_pos[1]
        dir_x, dir_y = self.normalize_vector2((dir_x, dir_y))
        # if self._vx < self.__max_vel and self._vy < self.__max_vel:
        # self._vx = dir_x * self.__speed
        # self._vy = dir_y * self.__speed
        self.throw(from_pos, 40)

    def get_health(self):
        return self.__health

    def set_health(self, health):
        self.__health = health

    def sub_health(self, health):
        self.__health -= health

    def add_health(self, health):
        self.__health += health

    def collidepoint(self, point):
        if self.rect.collidepoint(point):
            return True
        return False

    def colliderect(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False

    def get_rect(self):
        return self.rect
