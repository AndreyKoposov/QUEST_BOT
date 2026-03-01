from random import randint
from app.game.action import Action
from app.game.state import State
from app.game.structures import GameState, ActionResult
from .states_id import StateID


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
        res = ActionResult()

        # Атрибуты игры в карты
        bet = params.get("bet", 0)
        player_score = randint(1, 11)
        enemy_score = randint(1, 11)
        enemy_stoped = False

        res.add_msg(f"Вы решили поставить {bet} монет. Начнём!\
                    \nВы вытянули карту: {player_score} очков!")

        res.add_line(f"Игрок поставил на кон {bet} монет.")
        res.add_line(f"Игрок начал играть и вытянул карту стоимостью {player_score} очков.")
        res.add_line("Противник тоже взял карту.")

        # Передаем как параметры следующего состояния
        params["bet"] = bet
        params["player_score"] = player_score
        params["enemy_score"] = enemy_score
        params["enemy_stoped"] = enemy_stoped

        return res + game.location.change_state(game, StateID.CARDS_PLAY, params)
    @staticmethod
    def leave_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик отмены игры"""
        res = ActionResult(["Вы решили, что не хотите сейчас играть"])

        return res + game.location.change_state(game, StateID.ENTER, params)
    #endregion
    #region Buttons
    @staticmethod
    def no_bet_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры без ставки"""
        return CardsStart.start_game_action_handler(game, {})
    @staticmethod
    def small_bet_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры с маленькой ставкой"""
        return CardsStart.start_game_action_handler(game, {"bet": 5})
    @staticmethod
    def big_bet_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры с большой ставкой"""
        return CardsStart.start_game_action_handler(game, {"bet": 20})
    @staticmethod
    def leave_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки отмены"""
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

    @staticmethod
    def get_btns_menu() -> list[list[str]]:
        return [[CardsStart.no_bet_btn, CardsStart.small_bet_btn, CardsStart.big_bet_btn],
                [CardsStart.leave_btn]]

    @staticmethod
    def on_enter(game: GameState, params: dict) -> ActionResult:
        # Если ставка уже указана, то запускаем игру сразу
        bet = params.get("bet", None)
        if bet is not None:
            return CardsStart.start_game_action_handler(game, params)

        return ActionResult(["Вы решили сыграть в карты. На что играем?"])

    @staticmethod
    def on_exit(game: GameState, params: dict) -> ActionResult:
        return ActionResult()
