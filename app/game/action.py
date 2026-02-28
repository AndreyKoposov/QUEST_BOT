from __future__ import annotations
from typing import TYPE_CHECKING
from collections.abc import Callable
if TYPE_CHECKING:
    from app.game.structures import ActionResult, GameState


class Action:
    """Класс действия"""
    def __init__(self, action_id: str, handler: Callable, **args) -> None:
        self.id = action_id
        self.handler = handler
        self.params: dict[str, str] = args.get("params", {})
        self.required: list[str] = args.get("required", [])

    def execute(self, game, params) -> ActionResult:
        """Исполнение действия"""
        return self.handler(game, params)

    def get_template(self) -> str:
        """Возвращает шаблон для ИИ"""
        result = "{"
        for param, value in self.params.items():
            result += f'\n\t"{param}": {value}'
        result += "\n}"
        return result

    def get_context(self, game: GameState) -> str:
        """Возвращает контекст для ИИ"""
        result = f"Локация: {game.location.name}"

        if "npcs" in self.required:
            result += ", ".join([str(npc) for npc in game.location.npcs])

        return result
