import pygame

from game import settings
from game.entities.crosshair import Crosshair
from game.scenes.scene import Scene
from game.states.game_states import GameStates


class GameOverScene(Scene):

    def __init__(self, gsm, waves):
        super().__init__(gsm)

        # Crosshair
        self.__crosshair = Crosshair(settings.SCREEN_WIDTH / 2,
                                     settings.SCREEN_HEIGHT / 2,
                                     35, 35,
                                     settings.ui_res,
                                     'crosshair.png')

        # Fonts
        font_path = str(settings.fonts_res / 'dpcomic.ttf')
        self.__small_font = pygame.font.Font(font_path, 45)
        self.__large_font = pygame.font.Font(font_path, 100)

        # Title
        self.__title = self.__large_font.render("Game Over", True, (180, 200, 210))

        # Start text
        self.__button_text = self.__small_font.render("Restart", True, (255, 255, 255))

        # Waves text
        waves_text = f"Yor record: {waves} waves."
        self.__waves_text = self.__small_font.render(waves_text, True, (235, 235, 235))

        # Play Button
        button_press_path = str(settings.ui_res / "menu_button_press.png")
        button_rel_path = str(settings.ui_res / "menu_button.png")
        self.__button_props = (192, 64)
        self.__button_press_img = pygame.transform.scale(pygame.image.load(button_press_path), self.__button_props)
        self.__button_rel_img = pygame.transform.scale(pygame.image.load(button_rel_path), self.__button_props)
        self.__button_image = self.__button_rel_img
        self.__button_pressed = False

        # Positions
        self.__title_pos = (settings.SCREEN_WIDTH / 2 - self.__title.get_width() / 2,
                            settings.SCREEN_HEIGHT / 2 - self.__title.get_height() / 2 - 80)

        self.__button_pos = (settings.SCREEN_WIDTH / 2 - self.__button_props[0] / 2,
                             settings.SCREEN_HEIGHT / 2 - self.__button_props[1] / 2)

        self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 25,
                                  self.__button_pos[1] + self.__button_text.get_height() / 2 - 15)

        self.__waves_text_pos = (settings.SCREEN_WIDTH / 2 - self.__waves_text.get_width() / 2,
                                 settings.SCREEN_HEIGHT - 50)

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
        screen.blit(self.__title, self.__title_pos)
        screen.blit(self.__button_image, self.__button_pos)
        screen.blit(self.__button_text, self.__button_text_pos)
        screen.blit(self.__waves_text, self.__waves_text_pos)
        self.__crosshair.draw(screen)
        if self.__transition:
            screen.blit(self.__close_effect, (0, 0))

    def update(self, dt):
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
                self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 25,
                                          self.__button_pos[1] + self.__button_text.get_height() / 2 - 8)
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
                    self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 25,
                                              self.__button_pos[1] + self.__button_text.get_height() / 2 - 8)
            else:
                if self.__button_pressed:
                    self.__button_image = self.__button_rel_img
                    self.__button_pressed = False
                    self.__button_text_pos = (self.__button_pos[0] + self.__button_text.get_width() / 2 - 25,
                                              self.__button_pos[1] + self.__button_text.get_height() / 2 - 15)
                    if collude_button:
                        self.__transition = True
