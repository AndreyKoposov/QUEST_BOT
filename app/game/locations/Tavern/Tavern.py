from app.game.location import Location
from .states import Enter, SelectGame, CardsStart, CardsPlay


class Tavern(Location):
    """Класс таверны"""
    id = "tavern"
    name = "Таверна"
    desc = "Уютная таверна, где полно народу и играет музыка"

    state = "enter"
    states = {}
    context = {
        "game": {},
        "talk": {}
    }

    def __init__(self):
        self.states[Enter.id] = Enter()
        self.states[SelectGame.id] = SelectGame()
        self.states[CardsStart.id] = CardsStart()
        self.states[CardsPlay.id] = CardsPlay()
