from app.game.action import Action
from app.game.player import Player


class OrderFood(Action):
    """Действие заказа еды"""
    id = "order_food"
    name = "Заказать еды"

    def execute(self, player: Player, location, scene, params: dict):
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

class RentRoom(Action):
    """Действие снятия комнаты"""
    id = "rent_room"
    name = "Снять комнату"

    def execute(self, player: Player, location, scene, params: dict):
        hourse = params.get("hourse", 1)

        story = list[str]()

        if 1 <= hourse <= 24:
            player.money -= 2 * hourse
            player.fatigue += hourse
            story.append("\nИгрок поспал и восстановил свои силы!")
        else:
            story.append("\nСнимать комнату монжо только по часам, а не по суткам и минутам!")

class Talk(Action):
    """Действие снятия комнаты"""
    id = "talk"
    name = "Поговорить"

    def execute(self, player: Player, location, scene, params: dict):
        with_npc = params.get("with_npc", None)
        topic = params.get("topic", None)
        dialog_type = params.get("dialog_type", "normal")

        story = list[str]()

class Play(Action):
    """Действие игры"""
    id = "play"
    name = "Поиграть"

    def execute(self, player: Player, location, scene, params: dict):
        with_npc = params.get("with_npc", None)
        game_name = params.get("game_name", None)

        story = list[str]()

class LookAround(Action):
    """Осмотреться"""
    id = "look_around"
    name = "Осмотреться"

    def execute(self, player: Player, location, scene, params: dict):
        story = list[str]()
