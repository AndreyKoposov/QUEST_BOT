"""app"""
from app.game.action import Action
from app.game.scene import Scene


class Location:
    """Базовый класс локации"""
    id: str
    name: str
    description: str

    scenes: dict[str, Scene]
    button_actions: dict[str, str]
    ai_actions: dict[str, Action]
    npcs: list[str]
