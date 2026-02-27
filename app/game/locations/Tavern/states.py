from app.game.state import State
from app.game.action import Action
from app.game.result import ActionResult
from random import randint


class Enter(State):
    """Начальное состояние в таверне"""
    id = "enter"

    play = "🎲 Играть"

    @staticmethod
    def play_action_handler(player, location, params) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы сели за ближайший стол. Во что будем играть?"]

        return ActionResult(messages, [], new_state_id="play")

    @staticmethod
    def play_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Enter.play_action_handler(player, location, {})

    actions = {
        "play": Action("play", play_action_handler)
    }
    buttons = {
        play: play_btn_handler
    }

    def get_btns_menu(self) -> list[list[str]]:
        return [[self.play]]

class Play(State):
    """Выбор игры в таверне"""
    id = "play"

    cards = "🃏 Карты"
    dice = "🎲 Кости"
    leave = "❌ Вернуться"

    @staticmethod
    def cards_action_handler(player, location, params) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы решили сыграть в карты. Сколько ставим?"]

        return ActionResult(messages, [], new_state_id="cards")
    @staticmethod
    def dice_action_handler(player, location, params) -> ActionResult:
        """Обработчик действия игры"""
        messages = ["Вы решили сыграть в кости. Сколько ставим?"]

        return ActionResult(messages, [], new_state_id="dice")
    @staticmethod
    def leave_action_handler(player, location, params) -> ActionResult:
        """Обработчик действия отмены"""
        messages = ["Вы решили, что вам сегодня не до игр."]

        return ActionResult(messages, [], new_state_id="enter")

    @staticmethod
    def cards_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки выбора карт"""
        return Play.cards_action_handler(player, location, {})
    @staticmethod
    def dice_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки выбора костей"""
        return Play.dice_action_handler(player, location, {})
    @staticmethod
    def leave_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки отмены"""
        return Play.leave_action_handler(player, location, {})

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

class Cards(State):
    """Старт игры в карты"""
    id = "cards"

    no_bet = "🙅‍♂️ Без ставки"
    small_bet = "💰 Поставить 5 монет"
    big_bet = "💰💰 Поставить 20 монет"
    leave = "❌ Вернуться"

    @staticmethod
    def start_game_action_handler(player, location, params) -> ActionResult:
        """Обработчик действия игры"""
        bet = params.get("bet", 0)
        player_score = randint(1, 11)
        enemy_score = randint(1, 11)

        messages = [f"Вы решили поставить {bet} монет. Начнём!"]
        messages = [f"Вы вытянули карту: {player_score} очков!"]

        location.context["game"]["bet"] = bet
        location.context["game"]["player_score"] = player_score
        location.context["game"]["enemy_score"] = enemy_score

        return ActionResult(messages, [], new_state_id="cards_game")
    @staticmethod
    def leave_action_handler(player, location, params) -> ActionResult:
        """Обработчик отмены игры"""
        messages = ["Вы решили, что не хотите сейчас играть"]

        return ActionResult(messages, [], new_state_id="enter")

    @staticmethod
    def no_bet_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Cards.start_game_action_handler(player, location, {})
    @staticmethod
    def small_bet_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Cards.start_game_action_handler(player, location, {"bet": 5})
    @staticmethod
    def big_bet_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Cards.start_game_action_handler(player, location, {"bet": 20})
    @staticmethod
    def leave_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки игры"""
        return Cards.leave_action_handler(player, location, {})

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

class CardsGame(State):
    """Игра в карты"""
    id = "cards_game"

    take = "🃏 Ещё"
    stop = "❌ Пас"


    @staticmethod
    def take_action_handler(player, location, params) -> ActionResult:
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

        return ActionResult(messages, [], new_state_id="cards")
    @staticmethod
    def stop_action_handler(player, location, params) -> ActionResult:
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

        return ActionResult(messages, [], new_state_id="cards")

    @staticmethod
    def take_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки взятия карты"""
        return CardsGame.take_action_handler(player, location, {})
    @staticmethod
    def stop_btn_handler(player, location) -> ActionResult:
        """Обработчик кнопки паса"""
        return CardsGame.stop_action_handler(player, location, {})

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
