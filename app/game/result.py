class ActionResult():
    """Результат выполнения действия"""
    def __init__(self,
                 messages: list[str],
                 story: list[str],
                 new_state_id: str | None = None) -> None:

        self.messages = messages
        self.story = story
        self.new_state_id = new_state_id
