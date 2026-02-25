from app.game.location import Location
from app.game.scene import Scene
from app.game.player import Player


class GameSession:
    """Класс игровой сессии"""
    def __init__(self, player: Player):
        self.player = player
        self.current_location: Location
        self.current_scene: Scene

    def process_input(self, text: str):
        """Обработка ввода"""
        action = self.current_location.button_actions.get(text, None)

        if action is None:
            pass
        elif len(self.current_scene.available_actions) > 0 and action.id not in self.current_scene.available_actions:
            pass
        else:
            action.execute(self.player, self.current_location, self.current_scene, {})
