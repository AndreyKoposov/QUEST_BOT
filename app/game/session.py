from app.game.location import Location
from app.game.scene import Scene
from app.game.player import Player
from app.utils.preprocessor import Preprocessor
from app.ai.giga import GigaAI
from app.game.locations.Tavern.location import Tavern


class GameSession:
    """Класс игровой сессии"""
    def __init__(self, player: Player, GIGA: GigaAI):
        self.player = player
        self.current_location: Location
        self.current_scene: Scene
        self.__pr = Preprocessor()
        self.giga = GIGA

    def start(self) -> list[tuple[str, list[str] | None]]:
        self.current_location = Tavern()
        self.current_scene = self.current_location.scenes["enter"]

        return [(self.current_location.description, list(self.current_location.button_actions.keys()))]

    def process_input(self, text: str) -> list[tuple[str, list[str] | None]]:
        """Обработка ввода"""
        reply = []

        action_id = self.current_location.button_actions.get(text, None)

        if action_id is None:
            raw_response = self.giga.parse_action(text, self.current_location.name, self.current_scene.available_actions)
            action_id = self.__pr.preprocess(raw_response)["action"]
            action = self.current_location.ai_actions[action_id]

            raw_response = self.giga.parse(text, action.pattern, self.current_location, self.current_scene)
            action_params = self.__pr.preprocess(raw_response)
            result = action.execute(self.player, self.current_location, self.current_scene, action_params)
            if result.story:
                reply.append((result.story[0], None))

        elif len(self.current_scene.available_actions) > 0 and action_id not in self.current_scene.available_actions:
            reply.append(("Unknown action", None))
        else:
            action = self.current_location.ai_actions[action_id]
            result = action.execute(self.player, self.current_location, self.current_scene, {})
            if result.text:
                reply.append((result.text, None))

        return reply
    
