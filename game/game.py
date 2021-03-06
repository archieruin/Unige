import pygame

from game import settings
from game.states.game_states_manager import GameStatesManager
from game.states.game_states import GameStates


class Game:
    """Класс отвечающий за запуск игры и игровой цикл."""

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen_clear_color = (42, 40, 40)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        pygame.display.set_caption(settings.GAME_TITLE)
        game_icon = pygame.image.load(str(settings.ui_res / 'icon.png')).convert()
        pygame.display.set_icon(game_icon)

        # Inti game states manager
        self.__game_states_manager = GameStatesManager(GameStates.MAIN_MENU)
        self.__pause = False

        # Run game loop
        self.run()

    def run(self):
        while True:
            dt = self.clock.tick(settings.FPS) / 1000
            self.update(dt)
            self.draw()

    def draw(self):
        pygame.display.update()
        self.screen.fill(self.screen_clear_color)
        self.__game_states_manager.draw(self.screen)

    def update(self, dt):
        self.handle_events()
        self.__game_states_manager.update(dt)

    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.__game_states_manager.handle_events(events)


if __name__ == '__main__':
    game = Game()
