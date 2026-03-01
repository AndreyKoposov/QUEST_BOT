from __future__ import annotations
from typing import TYPE_CHECKING
from abc import abstractmethod
from collections.abc import Callable
if TYPE_CHECKING:
    from app.game.action import Action
    from app.game.structures import GameState, ActionResult


class State:
    """Базовый класс сцены"""
    id: str

    actions: dict[str, Action]
    buttons: dict[str, Callable]

    @staticmethod
    @abstractmethod
    def get_btns_menu() -> list[list[str]]:
        """Возвращает структурированный по столбцам и строкам список кнопок"""

    @staticmethod
    @abstractmethod
    def on_enter(game: GameState, params: dict) -> ActionResult:
        """Вызывается при входе в состояние"""

    @staticmethod
    @abstractmethod
    def on_exit(game: GameState, params: dict) -> ActionResult:
        """Вызывается при выходе из состояния"""
