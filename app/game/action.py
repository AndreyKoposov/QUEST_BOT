from app.game.result import ActionResult


class Action:
    """Базовый класс действия"""
    id: str
    name: str
    pattern: str

    def execute(self, player, location, scene, params: dict) -> ActionResult:
        """Исполнение действия"""
        return ActionResult()
