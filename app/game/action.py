from typing import Callable


class Action:
    """Базовый класс действия"""
    id: str
    name: str

    def execute(self, player, location, scene, params: dict):
        """Исполнение действия"""
