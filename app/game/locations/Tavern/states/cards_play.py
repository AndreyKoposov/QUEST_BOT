from random import randint
from app.game.structures import ActionResult, GameState
from app.game.action import Action
from app.game.state import State


class CardsPlay(State):
    """Игра в карты"""
    id = "cards_play"

    #region Aliases
    take_btn = "🃏 Ещё"
    stop_btn = "❌ Пас"

    take_action = "take_card"
    stop_action = "stop"
    #endregion
    #region Actions
    @staticmethod
    def take_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        player_score = game.location.context["game"]["player_score"]
        enemy_score = game.location.context["game"]["enemy_score"]
        enemy_stoped = game.location.context["game"].get("enemy_stoped", False)
        messages = []

        player_score += randint(1, 11)
        messages = [f"Вы взяли еще карту. Теперь ваш счет составляет: {player_score}"]

        if not enemy_stoped:
            if 11 < enemy_score < randint(1, 21) < 22:
                enemy_stoped = True
                messages.append("Противник пасует")
            else:
                enemy_score += randint(1, 11)
                messages.append("Противник берет еще")

        game.location.context["game"]["player_score"] = player_score
        game.location.context["game"]["enemy_score"] = enemy_score
        game.location.context["game"]["enemy_stoped"] = enemy_stoped

        if player_score < 22:
            return ActionResult(messages, [])

        while not enemy_stoped and enemy_score <= 21:
            if 11 < enemy_score < randint(1, 21) < 22:
                enemy_stoped = True
                messages.append("Противник пасует")
            else:
                enemy_score += randint(1, 11)
                messages.append("Противник берет еще")

        if player_score > 21 and enemy_score > 21 or player_score == enemy_score:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nНичья!")
        elif player_score > 21:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПроигрыш!")
        elif enemy_score > 21:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПобеда!")
        elif enemy_score > player_score:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПроигрыш!")
        else:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПобеда!")

        game.location.change_state(game, "cards_start", params)
        return ActionResult(messages, [])
    @staticmethod
    def stop_action_handler(game: GameState, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        player_score = game.location.context["game"]["player_score"]
        enemy_score = game.location.context["game"]["enemy_score"]
        enemy_stoped = game.location.context["game"].get("enemy_stoped", False)
        messages = []

        messages = ["Вы решили больше не брать карту"]

        while not enemy_stoped and enemy_score <= 21:
            if 11 < enemy_score < randint(1, 21) < 22:
                enemy_stoped = True
                messages.append("Противник пасует")
            else:
                enemy_score += randint(1, 11)
                messages.append("Противник берет еще")

        if player_score > 21 and enemy_score > 21 or player_score == enemy_score:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nНичья!")
        elif player_score > 21:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПроигрыш!")
        elif enemy_score > 21:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПобеда!")
        elif enemy_score > player_score:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПроигрыш!")
        else:
            messages.append(f"\nВаш счет {player_score}\nСчет противника {enemy_score}\nПобеда!")

        game.location.change_state(game, "cards_start", params)
        return ActionResult(messages, [])
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

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.take_btn, self.stop_btn]]

    def on_enter(self, game: GameState, params: dict):
        pass

    def on_exit(self, game: GameState, params: dict):
        pass
