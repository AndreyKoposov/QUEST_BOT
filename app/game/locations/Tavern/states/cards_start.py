from random import randint
from app.game.result import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.player import Player
from app.game.location import Location


class CardsStart(State):
    """Старт игры в карты"""
    id = "cards_start"

    no_bet = "🙅‍♂️ Без ставки"
    small_bet = "💰 Поставить 5 монет"
    big_bet = "💰💰 Поставить 20 монет"
    leave = "❌ Вернуться"

    @staticmethod
    def start_game_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        bet = params.get("bet", 0)
        player_score = randint(1, 11)
        enemy_score = randint(1, 11)
        enemy_stoped = False

        messages = [f"Вы решили поставить {bet} монет. Начнём!"]
        messages = [f"Вы вытянули карту: {player_score} очков!"]

        location.context["game"]["bet"] = bet
        location.context["game"]["player_score"] = player_score
        location.context["game"]["enemy_score"] = enemy_score
        location.context["game"]["enemy_stoped"] = enemy_stoped

        location.change_state(player, location, params, "cards_play")

        return ActionResult(messages, [])
    @staticmethod
    def leave_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик отмены игры"""
        messages = ["Вы решили, что не хотите сейчас играть"]

        location.change_state(player, location, params, "enter")

        return ActionResult(messages, [])

    @staticmethod
    def no_bet_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.start_game_action_handler(player, location, {})
    @staticmethod
    def small_bet_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.start_game_action_handler(player, location, {"bet": 5})
    @staticmethod
    def big_bet_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.start_game_action_handler(player, location, {"bet": 20})
    @staticmethod
    def leave_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.leave_action_handler(player, location, {})

    actions = {
        "start_game": Action("start_game", start_game_action_handler),
        "leave": Action("leave", leave_action_handler)
    }
    buttons = {
        no_bet: no_bet_btn_handler,
        small_bet: small_bet_btn_handler,
        big_bet: big_bet_btn_handler,
        leave: leave_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.no_bet, self.small_bet, self.big_bet], [self.leave]]
