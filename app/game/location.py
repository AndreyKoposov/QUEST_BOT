"""app"""
from app.game.action import Action
from app.game.scene import Scene


class Location:
    """Базовый класс локации"""
    id: str
    name: str
    description: str

    # Словарь доступных сцен (по умолчанию)
    scenes: dict[str, Scene]

    # Словари действий
    button_actions: dict[str, Action]  # Действия по кнопкам
    ai_actions: dict[str, None]   # Паттерны для ИИ
