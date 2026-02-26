"""app"""
from app.game.action import Action
from app.game.scene import Scene


class Location:
    """Базовый класс локации"""
    id: str
    name: str
    description: str

    scenes: dict[str, Scene]
    start_scene: str
    actions: dict[str, Action]
    npcs: list[str]

    def get_start_scene(self) -> Scene:
        """Возвращает стартовую сцену"""
        return self.scenes[self.start_scene]
