import pygame

from src import settings
from src.entities.crosshair import Crosshair
from src.entities.player import Player
from src.scenes.scene import Scene


class PlayScene(Scene):

    def __init__(self, gsm):
        super().__init__(gsm)
        # Crosshair
        self.__crosshair = Crosshair(settings.SCREEN_WIDTH / 2,
                                     settings.SCREEN_HEIGHT / 2,
                                     35, 35,
                                     settings.ui_res,
                                     'crosshair.png')

        # Player
        self.__player = Player(50, 50, 64, 64)

        # Pause
        self.__pause = False
        self.__pause_effect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.__pause_effect.set_alpha(200)
        self.__pause_effect.fill((0, 0, 0))

    def draw(self, screen):
        self.__player.draw(screen)
        self.__crosshair.draw(screen)

    def update(self, dt):
        if not self.__pause:
            self.__player.update()
        self.__crosshair.update()

    def handle_events(self):
        if not self.__pause:
            self.__player.handle_events(self.__crosshair)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not self.__pause:
                        self.__pause = True
                    else:
                        self.__pause = False
