from app.game.location import Location
from app.game.locations.Tavern.actions import Play, LookAround, RentRoom, OrderFood, Talk
from app.game.locations.Tavern.scenes import Enter, Dialog


class Tavern(Location):
    """Класс таверны"""
    id = "tavern"
    name = "Таверна"
    description = "Уютная таверна, можно отдохнуть, перекусить, поиграть, или снять комнату"

    scenes = {
        Enter.id: Enter(),
        Dialog.id: Dialog(),
    }
    button_actions = {
        "🎲 Играть": "play",
        "👀 Осмотреться": "look_around",
    }
    ai_actions = {
        "play": Play(),
        "look_around": LookAround(),
        "rent_room": RentRoom(),
        "order_food": OrderFood(),
        "talk": Talk()
    }
    npcs = ["Elsa", "Bard"]
