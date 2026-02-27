from app.game.location import Location
from app.game.locations.Tavern.states import Enter


class Tavern(Location):
    """Класс таверны"""
    id = "tavern"
    name = "Таверна"
    desc = "Уютная таверна"

    state = "enter"
    states = []
    context = {
        "game": {},
        "talk": {}
    }

    def __init__(self) -> None:
        self.states.append(Enter())
