class Character():
    def __init__(self) -> None:
        self.name = "Andrey"
        self.hp = 24
        self.max_hp = 30
        self.weapon = "Меч королей"
        self.armor = "Кольчуга"
        self.strength = 7
        self.agility = 5
        self.intellect = 5
        self.fatigue = 5
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
