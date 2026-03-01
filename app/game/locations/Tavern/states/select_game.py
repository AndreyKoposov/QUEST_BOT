from app.game.structures import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.structures import GameState
from .states_id import StateID


class SelectGame(State):
    """Выбор игры в таверне"""
    id = "select_game"

    #region Aliases
    cards_btn = "🃏 Карты"
    dice_btn = "🎲 Кости"
    leave_btn = "❌ Вернуться"

    cards_action = "play_cards"
    dice_action = "play_dice"
    leave_action = "leave"
    #endregion
    #region Actions
    @staticmethod
    def cards_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры в карты"""
        return game.location.change_state(game, StateID.CARDS_START, params)
    @staticmethod
    def dice_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры в кости"""
        return game.location.change_state(game, "dice_start", params)
    @staticmethod
    def leave_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия отмены"""
        res = ActionResult(["Вы решили, что вам сегодня не до игр."])

        return res + game.location.change_state(game, StateID.ENTER, params)
    #endregion
    #region Buttons
    @staticmethod
    def cards_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки выбора карт"""
        return SelectGame.cards_action_handler(game, {})
    @staticmethod
    def dice_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки выбора костей"""
        return SelectGame.dice_action_handler(game, {})
    @staticmethod
    def leave_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки отмены"""
        return SelectGame.leave_action_handler(game, {})
    #endregion

    actions = {
        cards_action: Action(cards_action, cards_action_handler),
        dice_action: Action(dice_action, dice_action_handler),
        leave_action: Action(leave_action, leave_action_handler)
    }
    buttons = {
        cards_btn: cards_btn_handler,
        dice_btn: dice_btn_handler,
        leave_btn: leave_btn_handler
    }

    @staticmethod
    def get_btns_menu() -> list[list[str]]:
        return [[SelectGame.cards_btn, SelectGame.dice_btn],
                [SelectGame.leave_btn]]

    @staticmethod
    def on_enter(game: GameState, params: dict) -> ActionResult:
        return ActionResult(["Вы сели за ближайший стол. Во что будеи играть?"])

    @staticmethod
    def on_exit(game: GameState, params: dict) -> ActionResult:
        return ActionResult()
