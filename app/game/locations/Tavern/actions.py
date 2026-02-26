from app.game.action import Action
from app.game.player import Player
from app.game.action import ActionResult
from app.ai.ai_pattern import AiPattern


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

        if food_type == "meat":
            player.strength += 1
            story.append("\nПерекусив, игрок повышает свою силу!")
        elif food_type == "soup":
            player.intellect += 1
            story.append("\nПерекусив, игрок повышает свой интеллект!")
        elif food_type == "dessert":
            player.agility += 1
            story.append("\nПерекусив, игрок повышает свою ловкость!")
        else:
            player.money += 5
            story.append("\nВ таверне не подают то, что заказал игрок.")

        if with_npc:
            story.append(f"\nПока игрок ел, он общался с {with_npc}.")

        text = "Вы поели"

        return ActionResult(text, story)

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

        if 1 <= hourse <= 24:
            player.money -= 2 * hourse
            player.fatigue += hourse
            story.append("\nИгрок поспал и восстановил свои силы!")
        else:
            story.append("\nСнимать комнату монжо только по часам, а не по суткам и минутам!")

        text = "Вы поспали"

        return ActionResult(text, story)

class Talk(Action):
    """Действие снятия комнаты"""
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

        return ActionResult(story=story)

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
        text = "Вы решили поиграть"

        return ActionResult(text, story)

class LookAround(Action):
    """Осмотреться"""
    id = "look_around"
    name = "Осмотреться"
    pattern = pattern = AiPattern(name, params={}, required_context=[])

    def execute(self, player: Player, location, scene, params: dict) -> ActionResult:
        story = list[str]()
        text = "Вы осмотрелись"

        return ActionResult(text, story)
