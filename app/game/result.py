class ActionResult():
    """Результат выполнения действия"""
    def __init__(self,
                 messages: list[str],
                 story: list[str]) -> None:

        self.messages = messages
        self.story = story
