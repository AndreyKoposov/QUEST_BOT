from app.game.scene import Scene


class Enter(Scene):
    """Сцена входа в таверну"""
    id = "enter"
    description = "Вы вошли в таверну, тут как всегда шумно и весело."

    available_actions = ["rent_room", "order_food", "talk", "play", "look_around"]

class Dialog(Scene):
    """Сцена разговора"""
    id = "dialog"
    description = "Вы разговариваете."

    available_actions = ["rent_room", "order_food"]
