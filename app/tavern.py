from location import Location


class Tavern(Location):
    def __init__(self) -> None:
        super().__init__()

        self.name = "Таверна"
        self.desc = "В таверне как всегда играла музыка и было полно народу."\
                    "За стойкой работала трактирщица, у нее можно снять комнату."
        self.actions = ["talk", "play", "rent_room"]
        self.npcs = list[str]()

    def get_menu(self) -> list[str]:
        return ["Снять комнату", "Сыграть в карты"]
    
    def do_action(self, game, action: str) -> str:
        return ""
        
    def do_option(self, game, option: str) -> str:
        return ""