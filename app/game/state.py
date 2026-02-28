from __future__ import annotations
from typing import TYPE_CHECKING
from abc import abstractmethod
from collections.abc import Callable
if TYPE_CHECKING:
    from app.game.action import Action
    from app.game.structures import GameState


class State:
    """Базовый класс сцены"""
    id: str

    actions: dict[str, Action]
    buttons: dict[str, Callable]

    @abstractmethod
    def get_btns_menu(self) -> list[list[str]]:
        """Возвращает структурированный список кнопок"""

    @abstractmethod
    def on_enter(self, game: GameState, params: dict):
        """Вызывается при входе в состояние"""

    @abstractmethod
    def on_exit(self, game: GameState, params: dict):
        """Вызывается при выходе из состояния"""
