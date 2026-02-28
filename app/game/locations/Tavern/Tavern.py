from app.game.location import Location
from .states import Enter, SelectGame, CardsStart, CardsPlay


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
        self.states.append(SelectGame())
        self.states.append(CardsStart())
        self.states.append(CardsPlay())
