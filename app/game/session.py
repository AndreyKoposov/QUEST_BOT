from app.game.location import Location
from app.game.player import Player
from app.utils.preprocessor import Preprocessor
from app.ai.giga import GigaAI
from app.game.locations.Tavern.location import Tavern
from app.game.action import Action


class GameSession:
    """Класс игровой сессии"""
    def __init__(self, ai: GigaAI):
        self.player: Player
        self.location: Location
        self.__pr = Preprocessor()
        self.__ai = ai

    def start(self) -> tuple[list[str], list[list[str]]]:
        """Старт игровой сессии"""
        self.player = Player()
        self.location = Tavern()

        return [self.location.desc], self.location.get_state().get_btns_menu()

    def process(self, text: str) -> tuple[list[str], list[list[str]]]:
        """Обработчик сообщения полььзователя"""
        if text in self.location.available_btns():
            result = self.location.perform(text, self.player, self.location)
        else:
            action, params = self.__extract_action(text)
            if action is None:
                return ["Unknown action"], self.location.get_state().get_btns_menu()
            result = action.execute(self.player, self.location, params)
            summery = self.__get_summery(text, result.story)
            result.messages.append(summery)

        return result.messages, self.location.get_state().get_btns_menu()

    def __extract_action(self, text: str) -> tuple[Action | None, dict]:
        """Свободный ввод"""
        raw_response = self.__ai.parse_action(text,
                                              self.location)
        action_id = self.__pr.preprocess(raw_response)["action"]

        if action_id not in self.location.available_actions():
            return None, {}

        action = self.location.get_state().actions[action_id]

        if len(action.params) == 0:
            return action, {}

        raw_response = self.__ai.parse_params(text,
                                              action,
                                              self.location)
        params = self.__pr.preprocess(raw_response)

        return action, params

    def __get_summery(self, text: str, story: list[str]) -> str:
        """Возвращает ответ ИИ на действие игрока"""
        context = "\nЛокация: " + self.location.name
        context = "\nРезультаты действия игрока:"
        for entry in story:
            context += "\n\t" + entry

        return self.__ai.summery(text, context)
