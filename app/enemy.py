class Enemy():
    def __init__(self, name: str, hp: int) -> None:
        self.name = name
        self.hp = hp
        self.max_hp = hp

        self.strength = 5
        self.agility = 5
        self.intellect = 5