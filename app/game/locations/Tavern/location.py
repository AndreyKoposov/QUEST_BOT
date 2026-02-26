from app.game.location import Location
from app.game.locations.Tavern.actions import Play, LookAround, RentRoom, OrderFood, Talk, LeaveCardGame, StartCardGame, OneMoreCard, ImOut
from app.game.locations.Tavern.scenes import Enter, Dialog, Cards


class Tavern(Location):
    """Класс таверны"""
    id = "tavern"
    name = "Таверна"
    description = "Уютная таверна, можно отдохнуть, перекусить, поиграть, или снять комнату"

    scenes = {
        Enter.id: Enter(),
        Dialog.id: Dialog(),
        Cards.id: Cards()
    }
    start_scene = Enter.id
    actions = {
        Play.id: Play(),
        LookAround.id: LookAround(),
        RentRoom.id: RentRoom(),
        OrderFood.id: OrderFood(),
        Talk.id: Talk(),
        LeaveCardGame.id: LeaveCardGame(),
        StartCardGame.id: StartCardGame(),
        OneMoreCard.id: OneMoreCard(),
        ImOut.id: ImOut()
    }
    npcs = ["Elsa", "Bard"]
