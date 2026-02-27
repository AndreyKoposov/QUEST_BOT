from collections.abc import Callable
from app.game.result import ActionResult


class Action:
    """Класс действия"""
    def __init__(self, action_id: str, handler: Callable, **args) -> None:
        self.id = action_id
        self.handler = handler
        self.params: dict[str, str] = args.get("params", {})
        self.required: list[str] = args.get("required", [])

    def execute(self, player, location, params) -> ActionResult:
        """Исполнение действия"""
        return self.handler(player, location, params)

    def get_template(self) -> str:
        """Возвращает шаблон для ИИ"""
        result = "{"
        for param, value in self.params.items():
            result += f'\n\t"{param}": {value}'
        result += "}"
        return result

    def get_context(self, location) -> str:
        """Возвращает контекст для ИИ"""
        result = f"Локация: {location.name}"

        if "npcs" in self.required:
            result += ", ".join([str(npc) for npc in location.npcs])

        return result
