from random import randint
from app.game.structures import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.structures import GameState


class CardsStart(State):
    """Старт игры в карты"""
    id = "cards_start"

    #region Aliases
    no_bet_btn = "🙅‍♂️ Без ставки"
    small_bet_btn = "💰 Поставить 5 монет"
    big_bet_btn = "💰💰 Поставить 20 монет"
    leave_btn = "❌ Вернуться"

    start_action = "start_game"
    leave_action = "leave"
    #endregion
    #region Actions
    @staticmethod
    def start_game_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        bet = params.get("bet", 0)
        player_score = randint(1, 11)
        enemy_score = randint(1, 11)
        enemy_stoped = False

        messages = [f"Вы решили поставить {bet} монет. Начнём!"]
        messages = [f"Вы вытянули карту: {player_score} очков!"]

        game.location.context["game"]["bet"] = bet
        game.location.context["game"]["player_score"] = player_score
        game.location.context["game"]["enemy_score"] = enemy_score
        game.location.context["game"]["enemy_stoped"] = enemy_stoped

        game.location.change_state(game, "cards_play", params)

        return ActionResult(messages, [])
    @staticmethod
    def leave_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик отмены игры"""
        messages = ["Вы решили, что не хотите сейчас играть"]

        game.location.change_state(game, "enter", params)

        return ActionResult(messages, [])
    #endregion
    #region Buttons
    @staticmethod
    def no_bet_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.start_game_action_handler(game, {})
    @staticmethod
    def small_bet_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.start_game_action_handler(game, {"bet": 5})
    @staticmethod
    def big_bet_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.start_game_action_handler(game, {"bet": 20})
    @staticmethod
    def leave_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры"""
        return CardsStart.leave_action_handler(game, {})
    #endregion

    actions = {
        start_action: Action(start_action, start_game_action_handler),
        leave_action: Action(leave_action, leave_action_handler)
    }
    buttons = {
        no_bet_btn: no_bet_btn_handler,
        small_bet_btn: small_bet_btn_handler,
        big_bet_btn: big_bet_btn_handler,
        leave_btn: leave_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.no_bet_btn, self.small_bet_btn, self.big_bet_btn], [self.leave_btn]]

    def on_enter(self, game: GameState, params: dict):
        bet = params.get("bet", None)
        if bet is not None:
            self.start_game_action_handler(game, params)

    def on_exit(self, game: GameState, params: dict):
        pass
