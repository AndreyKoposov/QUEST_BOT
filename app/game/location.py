"""app"""
from app.game.result import ActionResult
from app.game.state import State


class Location:
    """Базовый класс локации"""
    id: str
    name: str
    desc: str

    state: str
    states: list[State]
    context: dict

    npcs: list[str]
    interacts: list[str]
    events: list[str]

    def perform(self, btn_name: str, player, location) -> ActionResult:
        """Запускает обработчик кнопки"""
        btn_handler = self.get_state().buttons[btn_name]
        return btn_handler(player, location)

    def available_actions(self) -> list[str]:
        """Возвращает доступные действия"""
        return list(self.get_state().actions.keys())

    def available_btns(self) -> list[str]:
        """Возвращает доступные кнопки"""
        return list(self.get_state().buttons.keys())

    def get_state(self) -> State:
        """Возвращает текущее состояния"""
        return next(filter(lambda s: s.id == self.state, self.states))

    def change_state(self, player, location, params, state_id: str):
        """Сменяет состояние локации на новое"""
        self.get_state().on_exit(player, location, params)
        self.state = state_id
        self.get_state().on_enter(player, location, params)
