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
    start_scene = Enter.id
    actions = {
        Play.id: Play(),
        LookAround.id: LookAround(),
        RentRoom.id: RentRoom(),
        OrderFood.id: OrderFood(),
        Talk.id: Talk()
    }
    npcs = ["Elsa", "Bard"]
