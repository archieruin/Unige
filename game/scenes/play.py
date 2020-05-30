import random

import pygame
from pygame.sprite import Group

from game import settings
from game.entities.bullet import Bullet
from game.entities.crosshair import Crosshair
from game.entities.player import Player
from game.entities.slime import Slime
from game.scenes.scene import Scene


class PlayScene(Scene):

    def __init__(self, gsm):
        super().__init__(gsm)

        # Pause
        self.__pressed_pause = False
        self.__pause = False
        self.__pause_effect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.__pause_effect_alpha = 0
        self.__pause_effect.set_alpha(self.__pause_effect_alpha)
        self.__pause_effect.fill((0, 0, 0))

        # Crosshair
        self.__crosshair = Crosshair(settings.SCREEN_WIDTH / 2,
                                     settings.SCREEN_HEIGHT / 2,
                                     35, 35,
                                     settings.ui_res,
                                     'crosshair.png')

        # Groups
        self.__player_group = Group()
        self.__enemies_group = Group()
        self.__bullets_group = Group()

        # Player
        self.__player = Player(settings.SCREEN_WIDTH / 2 - 32, settings.SCREEN_HEIGHT / 2 - 32, 64, 64, 6)
        self.__player_group.add(self.__player)

        # Font
        font_path = str(settings.fonts_res / 'Arcade Classic.ttf')
        self.__health_font = pygame.font.Font(font_path, 32)
        health_text = "HP %d" % self.__player.get_health()
        self.__player_health = self.__health_font.render(health_text, True, (180, 200, 210))

        # Slimes
        slime_size = 48
        self.__slimes_count = 2
        for i in range(self.__slimes_count):
            pos_choices = 'top', 'down', 'left', 'right'
            pos_choice = random.choice(pos_choices)
            rand_x = 0
            rand_y = 0
            if pos_choice == 'top':
                rand_x = random.randint(-slime_size, settings.SCREEN_WIDTH - slime_size)
                rand_y = -slime_size
            elif pos_choice == 'down':
                rand_x = random.randint(-slime_size, settings.SCREEN_WIDTH - slime_size)
                rand_y = slime_size + settings.SCREEN_HEIGHT
            elif pos_choice == 'left':
                rand_x = -slime_size
                rand_y = random.randint(-slime_size, settings.SCREEN_HEIGHT + slime_size)
            elif pos_choice == 'right':
                rand_x = slime_size + settings.SCREEN_WIDTH
                rand_y = random.randint(-slime_size, settings.SCREEN_HEIGHT + slime_size)
            slime = Slime(rand_x, rand_y, slime_size, slime_size, 2)
            self.__enemies_group.add(slime)

    def draw(self, screen):
        self.__enemies_group.draw(screen)
        self.__player_group.draw(screen)
        screen.blit(self.__player_health, (10, 10))

        if self.__pause:
            screen.blit(self.__pause_effect, (0, 0))

        self.__crosshair.draw(screen)

    def update(self, dt):
        if not self.__pause:
            # Update Groups
            for enemy in self.__enemies_group.sprites():
                enemy.move_to_player(self.__player.get_pos())

                for other_enemy in self.__enemies_group.sprites():
                    if enemy.colliderect(other_enemy.get_rect()):
                        enemy.throw(other_enemy.get_pos())

                # Check collides between slimes and player
                if self.__player.colliderect(enemy.get_rect()):
                    self.__player.take_damage(enemy.get_pos(), 1)

            self.__player_group.update(dt)
            self.__enemies_group.update(dt)

            # Draw player health points
            health_text = "HP %d" % self.__player.get_health()
            self.__player_health = self.__health_font.render(health_text, True, (180, 200, 210))
        else:
            # Pause Effect
            if self.__pause_effect_alpha <= 128:
                self.__pause_effect_alpha += 5
                self.__pause_effect.set_alpha(self.__pause_effect_alpha)

        self.__crosshair.update(dt)

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

            if event.type == pygame.MOUSEBUTTONUP:
                player_x = self.__player.get_pos()[0]
                player_y = self.__player.get_pos()[1]
                mouse_pos = pygame.mouse.get_pos()
                bullet = Bullet(player_x, player_y, 16, (255, 0, 0), mouse_pos, speed=10)
                self.__bullets_group.add(bullet)