"""Модуль содержит структур данных игры"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.game.player import Player
    from app.game.location import Location


class ActionResult():
    """Результат выполнения действия"""
    def __init__(self, messages: list[str] | None = None,
                 story: list[str] | None = None) -> None:

        # Сообщения для игрока
        self.messages = messages if messages else list[str]()
        # Сводка для ИИ
        self.story = story if story else list[str]()

    def add_msg(self, msg: str):
        """Добавляет новое сообщение для игрока"""
        self.messages.append(msg)

    def add_line(self, line: str):
        """Добавляет новую запись в сводку для ИИ"""
        self.story.append(line)

    def __add__(self, other):
        if isinstance(other, ActionResult):
            messages = self.messages + other.messages
            story = self.story + other.story

            return ActionResult(messages, story)

        raise TypeError

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
