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

    @abstractmethod
    def get_btns_menu(self) -> list[list[str]]:
        """Возвращает структурированный по столбцам и строкам список кнопок"""

    @abstractmethod
    def on_enter(self, game: GameState, params: dict) -> ActionResult:
        """Вызывается при входе в состояние"""

    @abstractmethod
    def on_exit(self, game: GameState, params: dict) -> ActionResult:
        """Вызывается при выходе из состояния"""
