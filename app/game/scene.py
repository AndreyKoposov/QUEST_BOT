class Scene:
    """Базовый класс сцены"""
    id: str
    description: str

    # Какие действия доступны в этой сцене
    available_actions: list[str]

    # Данные сцены (кто NPC, какой предмет и т.д.)
    context: dict
