from math import sqrt

import pygame

from .entity import Entity
from .. import settings


class Player(Entity):
    
    def __init__(self, x, y, width, height, speed=5, health=10):
        super().__init__(x, y, width, height)
        self.__player_res = settings.player_res
        self.__speed = speed
        self.__health = health
        self.__hit_countdown = 0
        self.__dx = 0
        self.__dy = 0
        self.__vx = 0
        self.__vy = 0

        self.__got_damage = False

        self.watch_left = False
        self.watch_right = True

        self.move_top = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.idle = True

        self.__idle_anim = [
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f0.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f1.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f2.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f3.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f4.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_idle_anim_f5.png')), width, height)
        ]

        self.__move_anim = [
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f0.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f1.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f2.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f3.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f4.png')), width, height),
            self.scale(self.load(str(self.__player_res / 'knight_run_anim_f5.png')), width, height)
        ]

        self.__damage_image = self.scale(
            self.load(str(self.__player_res / 'knight_got_damage.png')), width, height)

        self.__anim = self.__idle_anim
        self.__frame = 0
        self.__image = self.__anim[int(self.__frame)]
        self.__original_image = self.__image
        self.__rect = self.__image.get_rect(topleft=self.get_pos())

    def draw(self, screen):
        screen.blit(self.__image, (self._x, self._y))
        # pygame.draw.rect(screen, (255, 0, 0), self.__rect)

    def update(self, dt):
        self.__frame += 0.2
        if self.__frame >= len(self.__anim):
            self.__frame = 0

        if self.watch_left:
            self.__image = self.h_flip(self.__anim[int(self.__frame)])
        else:
            self.__image = self.__anim[int(self.__frame)]
        self.__original_image = self.__image
        self.__rect = self.__image.get_rect(topleft=self.get_pos())

        if self.__hit_countdown:
            if self.__hit_countdown % 2:
                self.__image = self.__damage_image
            else:
                self.__image = self.__original_image
            self.__hit_countdown = max(0, self.__hit_countdown - 1)
        else:
            self.__vx = self.__dx * self.__speed
            self.__vy = self.__dy * self.__speed
        print(self.__hit_countdown)
        print(self.__got_damage)

        self._x += self.__vx
        self._y += self.__vy

        if not self.move_top and not self.move_down and not self.move_left and not self.move_right:
            self.__anim = self.__idle_anim
        else:
            self.__anim = self.__move_anim

    def take_damage(self, enemy_pos, damage):
        self.__got_damage = True
        self.__health -= damage
        self.__hit_countdown = 15
        self_pos = self.get_pos()
        dir_x = self_pos[0] - enemy_pos[0]
        dir_y = self_pos[1] - enemy_pos[1]
        dir_len = sqrt(pow(dir_x, 2) + pow(dir_y, 2))
        dir_x = dir_x / dir_len
        dir_y = dir_y / dir_len
        self.__vx = dir_x * 5
        self.__vy = dir_y * 5

    def get_rect(self):
        return self.__rect

    def collidepoint(self, point):
        if self.__rect.collidepoint(point):
            return True
        return False

    def colliderect(self, rect):
        if self.__rect.colliderect(rect):
            return True
        return False

    def handle_events(self, events, crosshair):
        keys = pygame.key.get_pressed()
        mouse_x = crosshair.get_center()[0]
        player_x = self.get_center()[0]

        if mouse_x > player_x:
            self.watch_right = True
            self.watch_left = False
        if mouse_x < player_x:
            self.watch_left = True
            self.watch_right = False

        if keys[pygame.K_w]:
            self.__dy = -1
            self.move_top = True
            self.move_down = False
            self.idle = False
        elif keys[pygame.K_s]:
            self.__dy = 1
            self.move_down = True
            self.move_top = False
            self.idle = False
        else:
            self.__dy = 0
            self.idle = True
            self.move_down = False
            self.move_top = False

        if keys[pygame.K_a]:
            self.__dx = -1
            self.move_left = True
            self.move_right = False
            self.idle = False
        elif keys[pygame.K_d]:
            self.__dx = 1
            self.move_right = True
            self.move_left = False
            self.idle = False
        else:
            self.__dx = 0
            self.idle = True
            self.move_right = False
            self.move_left = False
