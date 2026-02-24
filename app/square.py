from location import Location
from tavern import Tavern
from forge import Forge


class Square(Location):
    def __init__(self) -> None:
        super().__init__()

        self.name = "Площадь"
        self.desc = "Большая площадь, по левую сторону стоит таверна 'Уставший Странник',"\
                    "а по правую сторону знаменитая кузница Белетора. Куда пойдём?"
        self.actions = ["to_tavern", "to_forge"]
        self.npcs = list[str]()

    def get_menu(self) -> list[str]:
        return ["В таверну", "В кузню"]
    
    def do_action(self, game, action: str) -> str:
        if action == "to_tavern":
            game.location = Tavern()
            game.new_loc = True
            return "Вы пошли в таверну"
        elif action == "to_forge":
            game.new_loc = True
            game.location = Forge()
            return "Вы пошли в кузню"
        else:
            raise Exception("Unkown action")
        
    def do_option(self, game, option: str) -> str:
        if option == "В таверну":
            return self.do_action(game, "to_tavern")
        elif option == "В кузню":
            return self.do_action(game, "to_forge")
        else:
            raise Exception("Unkown option")