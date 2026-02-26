from app.game.scene import Scene


class AiPattern():

    def __init__(self, action: str, params: dict[str, str], required_context: list[str]) -> None:
        self.action: str = action
        self.params: dict[str, str] = params
        self.required_context: list[str] = required_context

    def __str__(self) -> str:
        json_template = "{\n"
        for name, value in self.params.items():
            json_template += f'\t"{name}": {value},\n'
        json_template += "}"

        return json_template

    def get_context(self, loc, sc) -> str:
        """Возвращает строку со всей инофрмацией для ИИ"""
        context_str = f"Игрок хочет: {self.action}"
        context_str += f"\nЛокация: {loc.name}"

        if "npcs" in self.required_context:
            context_str += "\nДоступные персонажи: " + ', '.join([str(npc) for npc in loc.npcs])

        return context_str
        