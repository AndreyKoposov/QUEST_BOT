class Location():
    def __init__(self) -> None:
        self.name = ""
        self.desc = ""
        self.actions = list[str]()
        self.npcs = list[str]()

    def get_menu(self) -> list[str]:
        """Вовзвращает меню локации"""
        return list[str]()

    def do_action(self, game, action: str) -> str:
        return ""
        
    def do_option(self, game, option: str) -> str:
        return ""