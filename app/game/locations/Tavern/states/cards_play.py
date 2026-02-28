from random import randint
from app.game.result import ActionResult
from app.game.action import Action
from app.game.state import State
from app.game.player import Player
from app.game.location import Location


class CardsPlay(State):
    """Игра в карты"""
    id = "cards_play"

    take = "🃏 Ещё"
    stop = "❌ Пас"

    @staticmethod
    def take_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        player_score = location.context["game"]["player_score"]
        enemy_score = location.context["game"]["enemy_score"]
        enemy_stoped = location.context["game"].get("enemy_stoped", False)
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

        location.context["game"]["player_score"] = player_score
        location.context["game"]["enemy_score"] = enemy_score
        location.context["game"]["enemy_stoped"] = enemy_stoped

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

        location.change_state(player, location, params, "cards_start")
        return ActionResult(messages, [])
    @staticmethod
    def stop_action_handler(player: Player, location: Location, params: dict) -> ActionResult:
        """Обработчик действия игры"""
        player_score = location.context["game"]["player_score"]
        enemy_score = location.context["game"]["enemy_score"]
        enemy_stoped = location.context["game"].get("enemy_stoped", False)
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

        location.change_state(player, location, params, "cards_start")
        return ActionResult(messages, [])

    @staticmethod
    def take_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки взятия карты"""
        return CardsPlay.take_action_handler(player, location, {})
    @staticmethod
    def stop_btn_handler(player: Player, location: Location) -> ActionResult:
        """Обработчик кнопки паса"""
        return CardsPlay.stop_action_handler(player, location, {})

    actions = {
        "take_card": Action("take_card", take_action_handler),
        "stop": Action("stop", stop_action_handler)
    }
    buttons = {
        take: take_btn_handler,
        stop: stop_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.take, self.stop]]
