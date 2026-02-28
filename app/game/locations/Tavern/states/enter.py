from app.game.result import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.player import Player
from app.game.location import Location


class Enter(State):
    """Начальное состояние в таверне"""
    id = "enter"

    #region Aliases
    play_btn = "🎲 Играть"

    play_action = "play"
    #endregion
    #region Actions
    @staticmethod
    def play_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы сели за ближайший стол. Во что будем играть?"]

        location.change_state(player, location, params, "select_game")

        return ActionResult(messages, [])
    #endregion
    #region Buttons
    @staticmethod
    def play_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Enter.play_action_handler(player, location, {})
    #endregion

    actions = {
        play_action: Action(play_action, play_action_handler)
    }
    buttons = {
        play_btn: play_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.play_btn]]

    def on_enter(self, player: Player, location: Location, params: dict):
        pass

    def on_exit(self, player: Player, location: Location, params: dict):
        pass
