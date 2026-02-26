from app.game.location import Location
from app.game.scene import Scene
from app.game.player import Player
from app.utils.preprocessor import Preprocessor
from app.ai.giga import GigaAI
from app.game.locations.Tavern.location import Tavern
from app.game.action import Action


class GameSession:
    """Класс игровой сессии"""
    def __init__(self, player: Player, ai: GigaAI):
        self.player = player
        self.current_location: Location
        self.current_scene: Scene
        self.__pr = Preprocessor()
        self.__ai = ai

    def start(self) -> list[tuple[str, list[str] | None]]:
        """Старт игровой сессии"""
        self.current_location = Tavern()
        self.current_scene = self.current_location.get_start_scene()

        return [(self.current_location.description,
                 self.current_scene.get_buttons())]

    def process_input(self, text: str) -> list[tuple[str, list[str] | None]]:
        """Обработка ввода"""
        reply = []

        if text in self.current_scene.get_buttons():
            action, params = self.get_button_action(text), {}
            ai = False
        else:
            action, params = self.extract_action(text)
            ai = True

        if action is None:
            reply.append(("Unknown action", None))
            return reply

        result = action.execute(self.player,
                                self.current_location,
                                self.current_scene,
                                params, ai)

        if result.text:
            reply.append((result.text, None))
        if result.story:
            summery = self.get_summery(text, result.story)
            reply.append((summery, None))
        if result.new_location_id:
            pass
        if result.new_scene_id:
            pass

        return reply

    def get_button_action(self, text: str) -> Action | None:
        """Если нажата кнопка"""
        action_id = self.current_scene.button_actions[text]
        action = self.try_get_action(action_id)

        return action

    def extract_action(self, text: str) -> tuple[Action | None, dict]:
        """Свободный ввод"""
        raw_response = self.__ai.parse_action(text,
                                              self.current_location.name,
                                              self.current_scene.available_actions)
        action_id = self.__pr.preprocess(raw_response)["action"]
        action = self.try_get_action(action_id)

        if action is None or len(action.pattern.params) == 0:
            return action, {}

        raw_response = self.__ai.parse_params(text,
                                              action.pattern,
                                              self.current_location,
                                              self.current_scene)
        params = self.__pr.preprocess(raw_response)

        return action, params

    def try_get_action(self, action_id: str) -> Action | None:
        """Возвращает команду, если возможно"""
        if action_id in self.current_scene.available_actions:
            return self.current_location.actions[action_id]
        return None

    def get_summery(self, text: str, story: list[str]) -> str:
        """Возвращает ответ ИИ на действие игрока"""
        context = text
        context += "\n" + self.current_location.name
        for entry in story:
            context += "\n" + entry

        return self.__ai.summery(text, context)
