class Scene:
    """Базовый класс сцены"""
    id: str
    description: str

    ai_actions: list[str]
    button_actions: dict[str, str]
    context: dict

    def get_buttons(self) -> list[str]:
        """Возвращает список кнопок"""
        return list(self.button_actions.keys())

    def is_valid_action(self, action_id: str) -> bool:
        """Вовращает допустимость действия"""
        return action_id in self.ai_actions or action_id in self.button_actions.values()
