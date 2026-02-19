from character import Character
from logger import Logger


class Game():
    def __init__(self) -> None:
        self.character = Character()
        self.location = "location"
        self.enemy = "enemy"
        self.floor = 1

    def act(self, actions: list) -> str:
        """Выполняет действия из списка"""
        Logger.info(actions)
        
        return str(self.character)
