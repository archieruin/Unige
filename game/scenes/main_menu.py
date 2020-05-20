import pygame

from game import settings
from game.entities.crosshair import Crosshair
from game.scenes.scene import Scene
from game.states.game_states import GameStates


class MainMenuScene(Scene):

    def __init__(self, gsm):
        super().__init__(gsm)

        # Crosshair
        self.__crosshair = Crosshair(settings.SCREEN_WIDTH / 2,
                                     settings.SCREEN_HEIGHT / 2,
                                     35, 35,
                                     settings.ui_res,
                                     'crosshair.png')

        # Player icon
        self.__player_size = 84
        self.__icon_bg_size = 144
        self.__icon_bg = pygame.transform.scale(
            pygame.image.load(str(settings.ui_res / 'icon_bg.png')), (self.__icon_bg_size, self.__icon_bg_size))
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

        self.__player_frame = 0
        self.__player_image = self.__player_anim[int(self.__player_frame)]

        # Title and Font
        font_path = str(settings.fonts_res / 'Arcade Classic.ttf')
        self.__large_font = pygame.font.Font(font_path, 100)
        self.__title = self.__large_font.render("Unige", True, (180, 200, 210))

        # Start text
        self.__small_font = pygame.font.Font(font_path, 45)
        self.__button_text = self.__small_font.render("Start", True, (255, 255, 255))

        # Play Button
        button_press_path = str(settings.ui_res / "menu_button_press.png")
        button_rel_path = str(settings.ui_res / "menu_button.png")
        self.__button_props = (192, 64)
        self.__button_press_img = pygame.transform.scale(pygame.image.load(button_press_path), self.__button_props)
        self.__button_rel_img = pygame.transform.scale(pygame.image.load(button_rel_path), self.__button_props)
        self.__button_image = self.__button_rel_img
        self.__button_pressed = False

        # Positions
        self.__icon_bg_pos = (settings.SCREEN_WIDTH / 2 - self.__icon_bg_size / 2,
                              settings.SCREEN_HEIGHT / 2 - self.__icon_bg_size / 2 - 120)

        self.__player_image_pos = (settings.SCREEN_WIDTH / 2 - self.__player_size / 2,
                                   settings.SCREEN_HEIGHT / 2 - self.__player_size / 2 - 120)

        self.__title_pos = (settings.SCREEN_WIDTH / 2 - self.__title.get_width() / 2 + 4,
                            settings.SCREEN_HEIGHT / 2 - self.__title.get_height() / 2)

        self.__button_pos = (settings.SCREEN_WIDTH / 2 - self.__button_props[0] / 2 + 5,
                             settings.SCREEN_HEIGHT / 2 - self.__button_props[1] / 2 + 80)

        self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 22,
                                  self.__button_pos[1] + 4)

        # Rects
        self.__button_rect = self.__button_image.get_rect(topleft=self.__button_pos)
        self.__button_text_rect = self.__button_text.get_rect(center=self.__button_text_pos)

        # Effects
        self.__ignore_mouse_clicks = False
        self.__transition = False
        self.__close_effect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.__close_effect_alpha = 0
        self.__close_effect.set_alpha(self.__close_effect_alpha)
        self.__close_effect.fill((10, 10, 10))

    def draw(self, screen):
        screen.blit(self.__icon_bg, self.__icon_bg_pos)
        screen.blit(self.__player_image, self.__player_image_pos)
        screen.blit(self.__title, self.__title_pos)
        screen.blit(self.__button_image, self.__button_pos)
        screen.blit(self.__button_text, self.__button_text_pos)
        self.__crosshair.draw(screen)
        if self.__transition:
            screen.blit(self.__close_effect, (0, 0))

    def update(self, dt):
        self.__player_frame += 0.15
        if self.__player_frame >= len(self.__player_anim):
            self.__player_frame = 0
        self.__player_image = self.__player_anim[int(self.__player_frame)]
        self.__crosshair.update(dt)
        if self.__transition:
            self.__close_effect_alpha += 10
            self.__close_effect.set_alpha(self.__close_effect_alpha)
            if self.__close_effect_alpha > 255 + 300:
                self._gsm.set_state(GameStates.PLAY)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] == 1:
            if not self.__button_pressed:
                self.__ignore_mouse_clicks = True
                self.__button_image = self.__button_press_img
                self.__button_pressed = True
                self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 22,
                                          self.__button_pos[1] + 10)
                self.__transition = True

        if not self.__ignore_mouse_clicks:
            press = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            collude_button = self.__button_rect.collidepoint(mouse_pos) or \
                             self.__button_text_rect.collidepoint(mouse_pos)
            if press[0]:
                if collude_button and not self.__button_pressed:
                    self.__button_image = self.__button_press_img
                    self.__button_pressed = True
                    self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 22,
                                              self.__button_pos[1] + 10)
            else:
                if self.__button_pressed:
                    self.__button_image = self.__button_rel_img
                    self.__button_pressed = False
                    self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 22,
                                              self.__button_pos[1] + 5)
                    if collude_button:
                        self.__transition = True
