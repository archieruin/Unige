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
        self.__pressed_pause = False
        self.__pause = False
        self.__pause_effect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.__pause_effect_alpha = 0
        self.__pause_effect.set_alpha(self.__pause_effect_alpha)
        self.__pause_effect.fill((0, 0, 0))

    def draw(self, screen):
        self.__player.draw(screen)
        self.__crosshair.draw(screen)
        if self.__pause:
            screen.blit(self.__pause_effect, (0, 0))

    def update(self, dt):
        if not self.__pause:
            self.__player.update()
        self.__crosshair.update()

        if self.__pause and self.__pause_effect_alpha <= 128:
            self.__pause_effect_alpha += 5
            self.__pause_effect.set_alpha(self.__pause_effect_alpha)

    def handle_events(self, events):
        if not self.__pause:
            self.__player.handle_events(self.__crosshair)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    if self.__pause:
                        self.__pause = False
                        self.__pause_effect_alpha = 0
                    else:
                        self.__pause = True


