"""Модуль содержит структур данных игры"""
from app.game.player import Player
from app.game.location import Location


class ActionResult():
    """Результат выполнения действия"""
    def __init__(self,
                 messages: list[str],
                 story: list[str]) -> None:

        self.messages = messages
        self.story = story

class GlobalContext():
    """Глобальный контекст игры"""
    def __init__(self) -> None:
        self.time: int
        self.weather: str
        self.day_time: str

class GameState():
    """Состояние игры"""
    def __init__(self) -> None:
        self.player: Player
        self.location: Location
        self.context: GlobalContext
