"""app"""
from __future__ import annotations
from typing import TYPE_CHECKING
from app.game.structures import ActionResult
if TYPE_CHECKING:
    from app.game.structures import GameState
    from app.game.state import State


class Location:
    """Базовый класс локации"""
    id: str
    name: str
    desc: str

    state: str
    states: dict[str, State]
    context: dict

    npcs: list[str]
    interacts: list[str]
    events: list[str]

    def perform(self, btn_name: str, game) -> ActionResult:
        """Запускает обработчик кнопки"""
        btn_handler = self.get_state().buttons[btn_name]
        return btn_handler(game)

    def available_actions(self) -> list[str]:
        """Возвращает доступные действия"""
        return list(self.get_state().actions.keys())

    def available_btns(self) -> list[str]:
        """Возвращает доступные кнопки"""
        return list(self.get_state().buttons.keys())

    def get_state(self) -> State:
        """Возвращает текущее состояния"""
        return self.states[self.state]

    def change_state(self, game: GameState, state_id: str, params: dict) -> ActionResult:
        """Сменяет состояние локации на новое"""
        res = ActionResult()

        res += self.get_state().on_exit(game, params)
        self.state = state_id
        res += self.get_state().on_enter(game, params)

        return res
