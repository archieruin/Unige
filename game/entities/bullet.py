import pygame
from pygame.sprite import Sprite

from game import settings
from game.entities.entity import Entity


class Bullet(Entity, Sprite):

    def __init__(self, x, y, radius, color, direction, speed=10):
        super().__init__(x, y, width=radius, height=radius)
        Sprite.__init__(self)
        self.__radius = radius
        self.__color = color
        self.__direction = self.normalize_vector2(direction)
        print(self.__direction)
        self.__speed = speed
        self.__vel_x = speed * -self.__direction[0]
        self.__vel_y = speed * -self.__direction[1]
        self.image = self.load(str(settings.bullets_res / 'bullet.png'))
        self.rect = self.image.get_rect(topleft=self.get_pos())

    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, (self._x, self._y), self.__radius)

    def update(self, dt):
        if self._x < settings.SCREEN_WIDTH and self._x > 0 and self._y < settings.SCREEN_HEIGHT and self._y > 0:
            self._x += self.__vel_x
            self._y += self.__vel_y
            self.rect = self.image.get_rect(topleft=self.get_pos())
        else:
            self.kill()
