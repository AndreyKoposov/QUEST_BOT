from app.game.action import Action
from app.game.player import Player
from app.game.action import ActionResult
from app.ai.ai_pattern import AiPattern
from random import randint


class OrderFood(Action):
    """Действие заказа еды"""
    id = "order_food"
    name = "Заказать еды"
    pattern = AiPattern(name, params=
        {
            "food_type": "(meat/soup/dessert/other)",
            "with_npc": "(имя персонажа)"
        },
        required_context=["npcs"]
    )

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        food_type = params.get("food_type", "meat")
        with_npc = params.get("with_npc", None)

        player.money -= 5
        story = list[str]()
        messages = list[str]()

        if food_type == "meat":
            player.strength += 1

            story.append("\nПерекусив, игрок повышает свою силу!")
            messages.append("Отведав сочного стейка вы чувствуете, как вас наполняют силыю"\
                        "\n+1 Силы на 1 час")
        elif food_type == "soup":
            player.intellect += 1

            story.append("\nПерекусив, игрок повышает свой интеллект!")
            messages.append("Горячий суп успокаивает вас, вы приходите в чувствою"\
                        "\n+1 Интеллекта на 1 час")
        elif food_type == "dessert":
            player.agility += 1

            story.append("\nПерекусив, игрок повышает свою ловкость!")
            messages.append("Насладившись сладостями, вы чувствуете себя намного активнее."\
                        "\n+1 Ловоксти на 1 час")
        else:
            player.money += 5
            story.append("\nВ таверне не подают то, что заказал игрок.")

        if with_npc:
            story.append(f"\nПока игрок ел, он общался с {with_npc}.")

        return ActionResult(messages, story)

class RentRoom(Action):
    """Действие снятия комнаты"""
    id = "rent_room"
    name = "Снять комнату"
    pattern = AiPattern(name, params=
        {
            "hours": "(количество часов)"
        },
        required_context=[]
    )

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        hourse = params.get("hourse", 1)

        story = list[str]()
        messages = list[str]()

        if 1 <= hourse <= 24:
            player.money -= 2 * hourse
            player.fatigue += hourse

            story.append("\nИгрок поспал и восстановил свои силы!")
            messages.append("Поспав, чилы вернулись к вам, а здоровье полностью восстановлено")
        else:
            story.append("\nСнимать комнату монжо только по часам, а не по суткам и минутам!")

        return ActionResult(messages, story)

class Talk(Action):
    """Действие разговора"""
    id = "talk"
    name = "Поговорить"
    pattern = AiPattern(name, params=
        {
            "topic": "(тема разговора)",
            "with_npc": "(имя персонажа)",
            "dialog_type": "(normal/agressive/friendly)"
        },
        required_context=["npcs"]
    )

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        with_npc = params.get("with_npc", None)
        topic = params.get("topic", None)
        dialog_type = params.get("dialog_type", "normal")

        story = list[str]()
        messages = list[str]()

        return ActionResult(messages, story, new_scene_id="dialog", scene_context=params)

class Play(Action):
    """Действие игры"""
    id = "play"
    name = "Поиграть"
    pattern = AiPattern(name, params=
        {
            "game_name": "(кубики/карты)",
            "with_npc": "(имя персонажа)"
        },
        required_context=["npcs"]
    )

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        with_npc = params.get("with_npc", None)
        game_name = params.get("game_name", None)

        story = list[str]()
        messages = list[str]()

        return ActionResult(messages, story, new_scene_id="cards", scene_context=params)

class LookAround(Action):
    """Осмотреться"""
    id = "look_around"
    name = "Осмотреться"
    pattern = AiPattern(name, params={}, required_context=[])

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        story = list[str]()
        messages = list[str]()

        story.append("Игрок осмотрелся и заметил дерущихся пьяниц!")
        messages.append("Вы осмотрелись")

        return ActionResult(messages, story)

class LeaveCardGame(Action):
    """Покинуть игру в карты"""
    id = "leave_card_game"
    name = "Покинуть игру в карты"
    pattern = AiPattern(name, params={}, required_context=[])

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        story = list[str]()
        messages = list[str]()

        story.append("Игрок отказался играть в карты")
        messages.append("Вы решили, что сегодня вам не до игр.")

        return ActionResult(messages, story, new_scene_id="enter")

class StartCardGame(Action):
    """Начать игру в карты"""
    id = "start_card_game"
    name = "Начать игру в карты"
    pattern = AiPattern(name, params=
        {
            "bet": "(количество денег на кону)"
        },
        required_context=[])

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        story = list[str]()
        messages = list[str]()

        scene.button_actions = {
            "🃏 Еще": OneMoreCard.id,
            "❌ Пас": ImOut.id,
        }
        scene.ai_actions = [OneMoreCard.id, ImOut.id]

        bet = params.get("bet", None)
        player_score = randint(1, 11)
        enemy_score = randint(1, 11)

        story.append(f"Игра началась, ставка = {bet}")
        story.append(f"Игрок взял карту номиналом {player_score}")

        messages.append(f"Игра началась, ваша карта {player_score}")

        scene.context["bet"] = bet
        scene.context["player_score"] = player_score
        scene.context["enemy_score"] = enemy_score

        return ActionResult(messages, story)

class OneMoreCard(Action):
    """Взять еще карту"""
    id = "one_more_card"
    name = "Взять еще карту"
    pattern = AiPattern(name, params={}, required_context=[])

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        story = list[str]()
        messages = list[str]()

        npc = scene.context.get("with_npc", None)
        player_score = scene.context.get("player_score")
        enemy_score = scene.context.get("enemy_score")
        bet = scene.context.get("bet", 0)

        new_card = randint(1, 11)
        story.append(f"Игрок вытащил карту номинала {new_card}")
        messages.append(f"Номинал вытянутой карты сосавляет {new_card}")
        player_score += new_card

        enemy_turn = randint(1, 21)
        if enemy_score < enemy_turn < 21:
            story.append(f"Оппонент {npc} решил не тянуть новую карту")
        else:
            new_card = randint(1, 11)
            story.append(f"Оппонент {npc} решил взять еще карту")
            messages.append("Возьму еще")
            enemy_score += new_card

        scene_id = "cards"

        if enemy_score > 21 and player_score > 21:
            story.append("У обоих игроков больше 21 очков. Ничья!")
            messages.append(f"Ваш счёт: {player_score}\nСчёт оппонента: {enemy_score}\nНичья!")
        elif enemy_score > 21:
            story.append("Оппонент проиграл. Игрок победил!")
            messages.append(f"Ваш счёт: {player_score}\nСчёт оппонента: {enemy_score}\nПобеда!\nПолучено денег {bet}")
            #player.money += bet
        elif player_score > 21:
            story.append("Игрок проиграл. Оппонент победил!")
            messages.append(f"Ваш счёт: {player_score}\nСчёт оппонента: {enemy_score}\nПроигрыш!\nПотеряно денег {bet}")
            #player.money -= bet
        else:
            scene.context["player_score"] = player_score
            scene.context["enemy_score"] = enemy_score
            scene_id = None

        return ActionResult(messages, story, new_scene_id=scene_id)

class ImOut(Action):
    """Не брать карту"""
    id = "im_out"
    name = "Не брать карту"
    pattern = AiPattern(name, params={}, required_context=[])

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        story = list[str]()
        messages = list[str]()

        npc = scene.context.get("with_npc", None)
        player_score = scene.context.get("player_score")
        enemy_score = scene.context.get("enemy_score")
        bet = scene.context.get("bet", 0)

        story.append("Игрок решил не тянуть карту")
        messages.append("Вы не стали брать карту")

        enemy_turn = randint(1, 21)
        if enemy_score < enemy_turn < 21:
            story.append(f"Оппонент {npc} решил не тянуть новую карту")
            messages.append("Я пас")
        else:
            new_card = randint(1, 11)
            story.append(f"Оппонент {npc} решил взять еще карту")
            messages.append("Возьму еще")
            enemy_score += new_card

        scene_id = "cards"

        if enemy_score > 21 and player_score > 21:
            story.append("У обоих игроков больше 21 очков. Ничья!")
            messages.append(f"Ваш счёт: {player_score}\nСчёт оппонента: {enemy_score}\nНичья!")
        elif enemy_score > 21:
            story.append("Оппонент проиграл. Игрок победил!")
            messages.append(f"Ваш счёт: {player_score}\nСчёт оппонента: {enemy_score}\nПобеда!\nПолучено денег {bet}")
            #player.money += bet
        elif player_score > 21:
            story.append("Игрок проиграл. Оппонент победил!")
            messages.append(f"Ваш счёт: {player_score}\nСчёт оппонента: {enemy_score}\nПроигрыш!\nПотеряно денег {bet}")
            #player.money -= bet
        else:
            scene.context["player_score"] = player_score
            scene.context["enemy_score"] = enemy_score
            scene_id = None

        return ActionResult(messages, story, new_scene_id=scene_id)