from __future__ import annotations
from typing import TYPE_CHECKING
from app.utils.preprocessor import Preprocessor
from app.game.player import Player
from app.game.structures import GameState
from .locations import Tavern
if TYPE_CHECKING:
    from app.ai.giga import GigaAI
    from app.game.action import Action


class GameSession:
    """Класс игровой сессии"""
    def __init__(self, ai: GigaAI):
        self.game = GameState()
        self.__pr = Preprocessor()
        self.__ai = ai

    def start(self) -> tuple[list[str], list[list[str]]]:
        """Старт игровой сессии"""
        self.game.player = Player()
        self.game.location = Tavern()

        return [self.game.location.desc], self.game.location.get_state().get_btns_menu()

    def process(self, text: str) -> tuple[list[str], list[list[str]]]:
        """Обработчик сообщения полььзователя"""
        if text in self.game.location.available_btns():
            result = self.game.location.perform(text, self.game)
        else:
            action, params = self.__extract_action(text)
            if action is None:
                return ["Unknown action"], self.game.location.get_state().get_btns_menu()
            result = action.execute(self.game, params)
            summery = self.__get_summery(text, result.story)
            result.messages.clear()
            result.messages.append(summery)

        return result.messages, self.game.location.get_state().get_btns_menu()

    def __extract_action(self, text: str) -> tuple[Action | None, dict]:
        """Свободный ввод"""
        raw_response = self.__ai.parse_action(text, self.game.location.available_actions())
        action_id = self.__pr.preprocess(raw_response)["action"]

        if action_id not in self.game.location.available_actions():
            return None, {}

        action = self.game.location.get_state().actions[action_id]

        if len(action.params) == 0:
            return action, {}

        raw_response = self.__ai.parse_params(text, action, self.game)
        params = self.__pr.preprocess(raw_response)

        return action, params

    def __get_summery(self, text: str, story: list[str]) -> str:
        """Возвращает ответ ИИ на действие игрока"""
        context = "\nЛокация: " + self.game.location.name
        context = "\nРезультаты действия игрока:"
        for entry in story:
            context += "\n\t" + entry

        return self.__ai.summery(text, context)
