import random

import pygame

from game import settings
from game.entities.crosshair import Crosshair
from game.entities.player import Player
from game.entities.slime import Slime
from game.scenes.scene import Scene


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

        # Slimes
        slime_size = 48
        self.__slimes_count = 5
        self.__slimes = []
        for i in range(self.__slimes_count):
            rand_x = random.randint(slime_size, settings.SCREEN_WIDTH - slime_size)
            rand_y = random.randint(slime_size, settings.SCREEN_HEIGHT - slime_size)
            rand_speed = random.randint(1, 4) * (random.randint(5, 10) * 0.1)
            self.__slimes.append(Slime(rand_x, rand_y, slime_size, slime_size, rand_speed))

        # Pause
        self.__pressed_pause = False
        self.__pause = False
        self.__pause_effect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.__pause_effect_alpha = 0
        self.__pause_effect.set_alpha(self.__pause_effect_alpha)
        self.__pause_effect.fill((0, 0, 0))

    def draw(self, screen):
        for slime in self.__slimes:
            slime.draw(screen)
        self.__player.draw(screen)
        self.__crosshair.draw(screen)
        if self.__pause:
            screen.blit(self.__pause_effect, (0, 0))

    def update(self, dt):
        if not self.__pause:
            for slime in self.__slimes:
                slime.update(dt)
                slime.move_to_player(self.__player.get_center())
            self.__player.update(dt)
        self.__crosshair.update(dt)

        if self.__pause and self.__pause_effect_alpha <= 128:
            self.__pause_effect_alpha += 5
            self.__pause_effect.set_alpha(self.__pause_effect_alpha)

    def handle_events(self, events):
        if not self.__pause:
            self.__player.handle_events(events, self.__crosshair)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    if self.__pause:
                        self.__pause = False
                        self.__pause_effect_alpha = 0
                    else:
                        self.__pause = True
