class Enemy():
    def __init__(self, name: str, hp: int, realtion: int) -> None:
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.relation = realtion