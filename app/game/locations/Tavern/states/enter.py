from app.game.action import Action
from app.game.state import State
from app.game.structures import GameState, ActionResult
from .states_id import StateID


class Enter(State):
    """Начальное состояние в таверне"""
    id = StateID.ENTER

    #region Aliases
    play_btn = "🎲 Играть"

    play_action = "play"
    #endregion
    #region Actions
    @staticmethod
    def play_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        res = ActionResult()
        res.add_line("Игрок решил поиграть в настольные игры")

        game_name = params.get("game_name", None)
        if game_name:
            # Если игрок сразу указал игру, то запускаем её
            if game_name == "карты":
                return game.location.change_state(game, StateID.CARDS_START, params)
            if game_name == "кубики":
                return game.location.change_state(game, "dice_start", params)
            res.add_line("Никто не понял, в какую именно игру игрок хочет сыграть")

        # Если нет, то переходим в меню выбора игры
        res += game.location.change_state(game, StateID.SELECT_GAME, params)

        return res
    #endregion
    #region Buttons
    @staticmethod
    def play_btn_handler(game: GameState) -> ActionResult:
        """Обработчик кнопки игры"""
        return Enter.play_action_handler(game, {})
    #endregion

    actions = {
        play_action: Action(play_action, play_action_handler, params=
                            {
                                "game_name": "(карты/кубики)",
                                "bet": "(ставка, количество монет; укажи 0, если игрок хочет играть на интерес)"
                            })
    }
    buttons = {
        play_btn: play_btn_handler
    }

    @staticmethod
    def get_btns_menu() -> list[list[str]]:
        return [[Enter.play_btn]]

    @staticmethod
    def on_enter(game: GameState, params: dict) -> ActionResult:
        return ActionResult(["Вы стоите в зале уютной таверны"])

    @staticmethod
    def on_exit(game: GameState, params: dict) -> ActionResult:
        return ActionResult()
