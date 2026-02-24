from location import Location


class Forge(Location):
    def __init__(self) -> None:
        super().__init__()

        self.name = "Кузница"
        self.desc = "По всей кузнице раздавались металлические звоны"\
                    "ударов молота Белетора. Повсюду разбросаны инструменты и материалы."
        self.actions = ["craft", "buy"]
        self.npcs = list[str]()

    def get_menu(self) -> list[str]:
        return ["Поработать на наковальне", "Купить снаряжение"]
    
    def do_action(self, game, action: str) -> str:
        return ""
        
    def do_option(self, game, option: str) -> str:
        return ""