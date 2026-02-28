from app.game.structures import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.structures import GameState


class Enter(State):
    """Начальное состояние в таверне"""
    id = "enter"

    #region Aliases
    play_btn = "🎲 Играть"

    play_action = "play"
    #endregion
    #region Actions
    @staticmethod
    def play_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы сели за ближайший стол. Во что будем играть?"]

        game.location.change_state(game, "select_game", params)

        return ActionResult(messages, [])
    #endregion
    #region Buttons
    @staticmethod
    def play_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры"""
        return Enter.play_action_handler(game, {})
    #endregion

    actions = {
        play_action: Action(play_action, play_action_handler)
    }
    buttons = {
        play_btn: play_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.play_btn]]

    def on_enter(self, game: GameState, params: dict):
        pass

    def on_exit(self, game: GameState, params: dict):
        pass
