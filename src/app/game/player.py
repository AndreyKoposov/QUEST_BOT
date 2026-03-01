class Player():
    """Класс персонажа"""
    def __init__(self) -> None:
        self.name = "Andrey"
        self.hp = 30
        self.max_hp = 30
        self.weapon = "sword"
        self.armor = "Кольчуга"
        self.strength = 6
        self.agility = 6
        self.intellect = 6
        self.fatigue = 1
        self.money = 145
        self.items = ["меч", "зелье", "веревка"]
        self.effects = [("ослеплен", 2), ("силен", 1)]

    def __str__(self) -> str:
        items_str = ""
        for item in self.items:
            items_str += item + ", "

        effects_str = ""
        for effect, value in self.effects:
            effects_str += f"{effect}({value}), "

        return  f"⚔️ {self.name} ({self.hp}/{self.max_hp}❤️)\n"\
                f"━━━━━━━━━━━━━━━━━━\n"\
                f"⚔️ {self.weapon} | 🛡 {self.armor}\n"\
                f"💪{self.strength} 🤸{self.agility} 📚{self.intellect}"\
                f"\n😴{self.fatigue}\n💰{self.money}\n"\
                f"━━━━━━━━━━━━━━━━━━\n"\
                f"🎒 {items_str}\n"\
                f"✨ {effects_str}"
