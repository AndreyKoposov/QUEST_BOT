class Location():
    def __init__(self, name: str, interacts: list[str], effects: list[str]) -> None:
        self.name = name
        self.interacts = interacts
        self.effects = effects