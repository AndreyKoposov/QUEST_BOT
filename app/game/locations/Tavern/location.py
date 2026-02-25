from app.game.location import Location
from app.game.locations.Tavern.actions import Play, LookAround
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
        "🎲 Играть": Play(),
        "👀 Осмотреться": LookAround(),
    }
