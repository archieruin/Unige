from pygame.sprite import Sprite

from game.entities.entity import Entity


class Bullet(Entity, Sprite):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        Sprite.__init__(self)


    def draw(self, screen):
        pass

    def update(self, dt):
        pass