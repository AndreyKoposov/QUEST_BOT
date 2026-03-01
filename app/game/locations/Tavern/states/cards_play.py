from random import randint
from app.game.structures import ActionResult, GameState
from app.game.action import Action
from app.game.state import State
from .states_id import StateID


class CardsPlay(State):
    """Игра в карты"""
    id = StateID.CARDS_PLAY
    bet: int # Ставка
    p_score: int # Очки игрока
    e_score: int # Очки противника
    e_stoped: bool # Противник пас?

    #region Aliases
    take_btn = "🃏 Ещё"
    stop_btn = "❌ Пас"

    take_action = "take_card"
    stop_action = "stop"
    #endregion
    #region Actions
    @staticmethod
    def take_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия взятия карты"""
        res = ActionResult()

        # Игрок берет карту
        CardsPlay.p_score += randint(1, 11)
        res.add_msg(f"Вы взяли еще карту. Теперь ваш счет составляет: {CardsPlay.p_score}")

        # Если противник еще не пасанул, то он делает ход
        if not CardsPlay.e_stoped:
            res += CardsPlay.__enemy_turn()

        # Если игрок перевалил за 21 очко, то он больше не ходит
        if CardsPlay.p_score > 21:
            res += CardsPlay.__end_game(game)
            return res + game.location.change_state(game, StateID.CARDS_START, params)

        return res
    @staticmethod
    def stop_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия паса"""
        res = ActionResult()
        res.add_msg("Вы решили больше не брать карту")
        res += CardsPlay.__end_game(game)

        return res + game.location.change_state(game, StateID.CARDS_START, params)
    #endregion
    #region Buttons
    @staticmethod
    def take_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки взятия карты"""
        return CardsPlay.take_action_handler(game, {})
    @staticmethod
    def stop_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки паса"""
        return CardsPlay.stop_action_handler(game, {})
    #endregion

    actions = {
        take_action: Action(take_action, take_action_handler),
        stop_action: Action(stop_action, stop_action_handler)
    }
    buttons = {
        take_btn: take_btn_handler,
        stop_btn: stop_btn_handler
    }

    @staticmethod
    def get_btns_menu() -> list[list[str]]:
        return [[CardsPlay.take_btn, CardsPlay.stop_btn]]

    @staticmethod
    def on_enter(game: GameState, params: dict) -> ActionResult:
        CardsPlay.bet = params["bet"]
        CardsPlay.p_score = params["player_score"]
        CardsPlay.e_score = params["enemy_score"]
        CardsPlay.e_stoped = params["enemy_stoped"]

        return ActionResult()

    @staticmethod
    def on_exit(game: GameState, params: dict) -> ActionResult:
        return ActionResult()

    @staticmethod
    def __end_game(game: GameState):
        res = ActionResult()

        # Просто для удобства
        player_score = CardsPlay.p_score
        enemy_score = CardsPlay.e_score

        # Противник ходит, пока не пасанет
        while not CardsPlay.e_stoped:
            CardsPlay.__enemy_turn()

        # Определение исхода игры
        if player_score > 21 and enemy_score > 21 or player_score == enemy_score:
            res.add_msg(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nНичья!")
        elif player_score > 21:
            res.add_msg(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПроигрыш!")
        elif enemy_score > 21:
            res.add_msg(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПобеда!")
        elif enemy_score > player_score:
            res.add_msg(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПроигрыш!")
        else:
            res.add_msg(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПобеда!")

        return res

    @staticmethod
    def __enemy_turn() -> ActionResult:
        res = ActionResult()

        # Чем больше у противника очков, тем выше шанс, что он пасанет
        if 11 < CardsPlay.e_score < randint(1, 21) < 22 or CardsPlay.e_score >= 21:
            CardsPlay.e_stoped = True
            res.add_msg("Противник пасует")
        else:
            CardsPlay.e_score += randint(1, 11)
            res.add_msg("Противник берет еще")

        return res
