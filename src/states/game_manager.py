from src.scenes.game_over_scene import GameOverScene
from src.scenes.main_menu_scene import MainMenuScene
from src.scenes.play_scene import PlayScene
from src.scenes.scene import Scene
from src.states.game_states import GameStates


class GameStatesManager:
    def __init__(self, state: GameStates):
        self.__state = state
        self.scene = self.set_state(self.__state)

    def update(self, dt):
        self.scene.update(dt)

    def draw(self, screen):
        self.scene.draw(screen)

    def handle_events(self):
        self.scene.handle_events()

    def set_state(self, state: GameStates) -> Scene:
        return self.get_scene(state)

    def get_scene(self, state: GameStates):
        if state == GameStates.MAIN_MENU:
            self.__state = GameStates.MAIN_MENU
            return MainMenuScene()
        elif state == GameStates.PLAY:
            self.__state = GameStates.PLAY
            return PlayScene()
        elif state == GameStates.GAME_OVER:
            self.__state = GameStates.GAME_OVER
            return GameOverScene()
