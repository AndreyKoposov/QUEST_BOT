from abc import abstractmethod
from collections.abc import Callable
from app.game.action import Action


class State:
    """Базовый класс сцены"""
    id: str

    actions: dict[str, Action]
    buttons: dict[str, Callable]

    @abstractmethod
    def get_btns_menu(self) -> list[list[str]]:
        """Возвращает структурированный список кнопок"""
