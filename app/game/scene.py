class Scene:
    """Базовый класс сцены"""
    id: str
    description: str

    available_actions: list[str]
    button_actions: dict[str, str]
    context: dict

    def get_buttons(self) -> list[str]:
        """Возвращает список кнопок"""
        return list(self.button_actions.keys())
