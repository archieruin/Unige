from abc import ABC, abstractmethod
from math import sqrt

import pygame


class Entity(ABC):

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._vx = 0
        self._vy = 0
        self._width = width
        self._height = height

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError

    @abstractmethod
    def update(self, dt):
        raise NotImplementedError

    def get_pos(self):
        return self._x, self._y

    def set_pos(self, x, y):
        self._x = x
        self._y = y

    def get_width(self):
        return self._width

    def set_width(self, width):
        self._width = width

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def get_center(self):
        return self._x + self._width / 2, self._y + self._height / 2

    @staticmethod
    def normalize_vector2(vec2):
        dir_len = sqrt(pow(vec2[0], 2) + pow(vec2[1], 2))
        dir_x = vec2[0] / dir_len
        dir_y = vec2[1] / dir_len
        return dir_x, dir_y

    @staticmethod
    def load(path):
        return pygame.image.load(path)

    @staticmethod
    def load_i_hflip(path):
        return Entity.h_flip(pygame.image.load(path))

    @staticmethod
    def h_flip(img):
        return pygame.transform.flip(img, True, False)

    @staticmethod
    def v_flip_img(img):
        return pygame.transform.flip(img, False, True)

    @staticmethod
    def scale(img, width, height):
        return pygame.transform.scale(img, (width, height))
