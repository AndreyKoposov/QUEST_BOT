from app.game.state import State
from app.game.action import Action
from app.game.result import ActionResult


class Enter(State):
    """Начальное состояние в таверне"""
    id = "enter"

    play = "🎲 Играть"

    @staticmethod
    def play_action_handler(player, location, params) -> ActionResult:
        """Обработчик действия игры"""
        print(player.hp)
        print(location.name)
        print(params)

        return ActionResult([], [])

    @staticmethod
    def play_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Enter.play_action_handler(player, location, {})

    actions = {
        "play": Action("play", play_action_handler)
    }
    buttons = {
        play: play_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.play]]
