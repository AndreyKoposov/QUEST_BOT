from app.game.result import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.player import Player
from app.game.location import Location


class SelectGame(State):
    """Выбор игры в таверне"""
    id = "select_game"

    cards = "🃏 Карты"
    dice = "🎲 Кости"
    leave = "❌ Вернуться"

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

    actions = {
        "play_cards": Action("play_cards", cards_action_handler),
        "play_dice": Action("play_dice", dice_action_handler),
        "leave": Action("leave", leave_action_handler)
    }
    buttons = {
        cards: cards_btn_handler,
        dice: dice_btn_handler,
        leave: leave_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.cards, self.dice], [self.leave]]
