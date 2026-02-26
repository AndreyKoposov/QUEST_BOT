class ActionResult():
    """Результат выполнения действия"""
    def __init__(self,
                 messages: list[str],
                 story: list[str],
                 new_location_id: str | None = None,
                 save_location: bool = False,
                 new_scene_id: str | None = None,
                 scene_context: dict | None = None,) -> None:

        self.messages = messages
        self.story = story
        self.new_location_id = new_location_id
        self.save_location = save_location
        self.new_scene_id = new_scene_id
        self.scene_context = scene_context
