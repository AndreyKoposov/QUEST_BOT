from app.game.scene import Scene
from app.game.locations.Tavern.actions import RentRoom, Play, LookAround, Talk, OrderFood


class Enter(Scene):
    """Сцена входа в таверну"""
    id = "enter"
    description = "Вы вошли в таверну, тут как всегда шумно и весело."

    available_actions = [RentRoom.id, OrderFood.id, Play.id, LookAround.id, Talk.id]
    button_actions = {
        "🎲 Играть": Play.id,
        "👀 Осмотреться": LookAround.id,
    }

class Dialog(Scene):
    """Сцена разговора"""
    id = "dialog"
    description = "Вы разговариваете."

    available_actions = [RentRoom.id, OrderFood.id]
    button_actions = {
        "💤 Снять комнату": RentRoom.id,
        "🍴 Заказать еду": OrderFood.id,
    }
