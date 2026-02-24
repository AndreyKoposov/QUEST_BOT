from character import Character
from location import Location
from square import Square
from enemy import Enemy
from logger import Logger
import random


class Game():
    def __init__(self) -> None:
        self.character = Character()
        self.location = Location()
        self.new_loc = False

    def start(self):
        self.location = Square()

    def get_menu(self) -> list[str]:
        return self.location.get_menu()
    
    def do_option(self, option: str) -> str:
        return self.location.do_option(self, option)

    def do_action(self, action: str) -> str:
        return self.location.do_action(self, action)