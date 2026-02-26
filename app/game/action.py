from app.game.result import ActionResult
from app.ai.ai_pattern import AiPattern


class Action:
    """Базовый класс действия"""
    id: str
    name: str
    pattern: AiPattern

    def execute(self, player, location, scene, params: dict) -> ActionResult:
        """Исполнение действия"""
        return ActionResult()
