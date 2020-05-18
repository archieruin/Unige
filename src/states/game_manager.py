from src.scenes.game_over_scene import GameOverScene
from src.scenes.main_menu_scene import MainMenuScene
from src.scenes.play_scene import PlayScene
from src.scenes.scene import Scene
from src.states.game_states import GameStates


class GameStatesManager:
    def __init__(self, state: GameStates):
        self.__state = state
        self.__scene = self.set_state(self.__state)

    def update(self, dt):
        self.__scene.update(dt)

    def draw(self, screen):
        self.__scene.draw(screen)

    def handle_events(self, events):
        self.__scene.handle_events(events)

    def set_state(self, state: GameStates):
        self.__scene = self.__get_scene(state)
        return self.__scene

    def get_state(self):
        return self.__state

    def __get_scene(self, state: GameStates):
        if state == GameStates.MAIN_MENU:
            self.__state = GameStates.MAIN_MENU
            return MainMenuScene(self)
        elif state == GameStates.PLAY:
            self.__state = GameStates.PLAY
            return PlayScene(self)
        elif state == GameStates.GAME_OVER:
            self.__state = GameStates.GAME_OVER
            return GameOverScene(self)
