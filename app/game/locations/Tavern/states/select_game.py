from app.game.result import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.player import Player
from app.game.location import Location


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
    def cards_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы решили сыграть в карты. Сколько ставим?"]

        location.change_state(player, location, params, "cards_start")

        return ActionResult(messages, [])
    @staticmethod
    def dice_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы решили сыграть в кости. Сколько ставим?"]

        location.change_state(player, location, params, "dice_start")

        return ActionResult(messages, [])
    @staticmethod
    def leave_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия отмены"""
        messages = ["Вы решили, что вам сегодня не до игр."]

        location.change_state(player, location, params, "enter")

        return ActionResult(messages, [])
    #endregion
    #region Buttons
    @staticmethod
    def cards_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки выбора карт"""
        return SelectGame.cards_action_handler(player, location, {})
    @staticmethod
    def dice_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки выбора костей"""
        return SelectGame.dice_action_handler(player, location, {})
    @staticmethod
    def leave_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки отмены"""
        return SelectGame.leave_action_handler(player, location, {})
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

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.cards_btn, self.dice_btn], [self.leave_btn]]

    def on_enter(self, player: Player, location: Location, params: dict):
        pass

    def on_exit(self, player: Player, location: Location, params: dict):
        pass
