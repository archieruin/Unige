from pathlib import Path

import pygame

from src.events_listener import EventsListener
from src.entities.crosshair import Crosshair
from src.entities.player import Player

root_dir = Path.cwd().parent
doc_dir = root_dir / 'doc/'
src_dir = root_dir / 'src/'
res_dir = root_dir / 'res/'

player_res = res_dir / 'player'


class Game:
    """Класс отвечающий за запуск игры и игровой цикл."""

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.game_title = 'Unige'
        self.fps = 60

        self.screen_width = 840
        self.screen_height = 650
        self.screen_clear_color = (52, 50, 50)

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.game_title)
        game_icon = pygame.image.load(str(res_dir / 'icon.png')).convert()
        pygame.display.set_icon(game_icon)

        # Init game entities
        self.crosshair = Crosshair(self.screen_width / 2, self.screen_height / 2, 35, 35, res_dir)
        self.player = Player(self.screen_width / 2, self.screen_height / 2, 60, 60, speed=5, player_res=player_res)

        self.events_listener = EventsListener(self)

        # Run game loop
        self.run()

    def run(self):
        while True:
            delta_time = self.clock.tick(self.fps) / 1000
            self.update()
            self.draw()

    def update(self):
        self.events_listener.update()
        self.crosshair.update()
        self.player.update()

    def draw(self):
        pygame.display.update()
        self.screen.fill(self.screen_clear_color)
        self.player.draw(self.screen)
        self.crosshair.draw(self.screen)


if __name__ == '__main__':
    game = Game()
