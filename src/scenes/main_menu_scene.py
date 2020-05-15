import pygame

from src import settings
from src.entities.crosshair import Crosshair
from src.scenes.scene import Scene


class MainMenuScene(Scene):

    def __init__(self):
        self.__player_size = 64
        self.__icon_bg = pygame.transform.scale(
            pygame.image.load(str(settings.ui_res / 'icon_bg.png')), (124, 124))
        self.__crosshair = Crosshair(settings.SCREEN_WIDTH / 2,
                                     settings.SCREEN_HEIGHT / 2,
                                     35, 35,
                                     settings.ui_res,
                                     'crosshair.png')
        self.__player_anim = [
            pygame.image.load(str(settings.player_res / 'knight_run_anim_f0.png')),
            pygame.image.load(str(settings.player_res / 'knight_run_anim_f1.png')),
            pygame.image.load(str(settings.player_res / 'knight_run_anim_f2.png')),
            pygame.image.load(str(settings.player_res / 'knight_run_anim_f3.png')),
            pygame.image.load(str(settings.player_res / 'knight_run_anim_f4.png')),
            pygame.image.load(str(settings.player_res / 'knight_run_anim_f5.png'))
        ]
        for i, img in enumerate(self.__player_anim):
            self.__player_anim[i] = pygame.transform.scale(img, (self.__player_size, self.__player_size))

        self.__current_frame = 0
        self.__image = self.__player_anim[int(self.__current_frame)]

    def draw(self, screen):
        screen.blit(self.__icon_bg, (settings.SCREEN_WIDTH / 2 - 124 / 2, 100))
        screen.blit(self.__image, (settings.SCREEN_WIDTH / 2 - self.__player_size / 2, 130))
        self.__crosshair.draw(screen)

    def update(self, dt):
        self.__current_frame += 0.15
        if self.__current_frame >= len(self.__player_anim):
            self.__current_frame = 0
        self.__image = self.__player_anim[int(self.__current_frame)]
        self.__crosshair.update()

    def handle_events(self):
        pass
