from src.entities.entity import Entity


class Button(Entity):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update(self):
        pass

    def draw(self, screen):
        pass
