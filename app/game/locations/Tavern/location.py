from app.game.location import Location
from app.game.locations.Tavern.states import Enter, Play, Cards, CardsGame


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
        self.states.append(Play())
        self.states.append(Cards())
        self.states.append(CardsGame())
