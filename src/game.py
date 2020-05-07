from pathlib import Path

import pygame

root_dir = Path.cwd().parent
src_dir = root_dir / 'src'
res_dir = root_dir / 'res'
doc_dir = root_dir / 'doc'


class Game:
    """Класс отвечающий за запуск игры и игровой цикл."""

    def __init__(self):
        self.game_title = 'Unige'
        self.fps = 60
        self.screen_width = 600
        self.screen_height = 320
        self.screen_clear_color = (52, 50, 50)

    def startup(self):
        pygame.init()
        display = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.game_title)
        clock = pygame.time.Clock()
        self.game_run(display, clock)

    def game_run(self, display, clock):
        while True:
            pygame.display.update()
            display.fill(self.screen_clear_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()

            clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.startup()
