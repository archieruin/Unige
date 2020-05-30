import pygame
from pygame.sprite import Sprite

from game import settings
from game.entities.entity import Entity


class Bullet(Entity, Sprite):

    def __init__(self, x, y, radius, color, direction, speed=10):
        super().__init__(x, y, width=radius, height=radius)
        Sprite.__init__(self)
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__color = color
        self.__direction = self.normalize_vector2(direction)
        self.__speed = speed
        self.__vel_x = speed * self.__direction
        self.__vel_y = speed * self.__direction
        self.image = self.__anim[int(self.__frame)]
        self.rect = self.image.get_rect(topleft=self.get_pos())

    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, (self.__x, self.__y), self.__radius)

    def update(self, dt):
        if settings.SCREEN_WIDTH > self.__x > 0 and settings.SCREEN_HEIGHT > self.__y > 0:
            self.__x += self.__vel_x
            self.__y += self.__vel_y
        else:
            self.kill()
