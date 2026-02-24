from character import Character
from location import Location
from enemy import Enemy
from logger import Logger
import random


class Game():
    actions = ["attack", "defend", "move", "talk", "wait", "explore", "item_use", "item_drop"]

    def __init__(self) -> None:
        self.character = Character()
        self.location = None
        self.enemy = None
        self.floor = 0

    def get_targets(self) -> list[str]:
        if self.enemy:
            targets = [self.enemy.name]
        else:
            targets = []
        return targets
    
    def get_items(self) -> list[str]:
        items = [self.character.weapon]
        return items
    
    def fight_info(self) -> str:
        if not self.enemy:
            return ""
        return  f"⚔️ {self.character.name} ({self.character.hp}/{self.character.max_hp}❤️)\n"\
                f"⚔️ {self.enemy.name} ({self.enemy.hp}/{self.enemy.max_hp}❤️)\n"\

    def act(self, actions: list) -> str:
        """Выполняет действия из списка"""
        Logger.info(actions)

        results = ""
        for action_data in actions:
            results += self.__act(action_data)

        return results

    def next_floor(self) -> str:
        """Метод для перехода на следующий этаж"""
        self.floor += 1

        self.location = self.__get_location()
        self.enemy = self.__get_enemy()

        return  f"Этаж {self.floor}\n"\
                f"На следующем этаже вы попали в {self.location.name}\n"\
                f"В комнате вы видите {', '.join([str(i) for i in self.location.interacts])}"\
                f"Особые эффекты комнаты: {', '.join([str(e) for e in self.location.effects])}"\
                f"Дорогу вам преградил {self.enemy.name}!"\

    def __get_location(self) -> Location:
        return Location("storage", ["chest", "giant_box"], ["greed", "closeness"])

    def __get_enemy(self) -> Enemy:
        return Enemy("goblin", 20)

    def __act(self, action_data: dict) -> str:
        action = action_data.get("action", None)
        target = action_data.get("target", None)
        item = action_data.get("item_used", None)

        if action is None or action not in Game.actions:
            Logger.error(f"Unknown action '{action}'")
            return "I dont understand"

        results = ""

        if action == "attack":
            results = self.__process_attack(action_data, target, item)

        return results

    def __process_attack(self, action_data: dict, target, item) -> str:
        attack_attrs = action_data.get("attack_attrs", None)
        force = "normal"
        aimed_to = "body"

        if attack_attrs:
            force = attack_attrs.get("force", force)
            aimed_to = attack_attrs.get("aimed_to", aimed_to)

        if self.enemy and target == self.enemy.name:
            results = self.__attack(item, force, aimed_to)
        else:
            results = ""

        return results

    def __attack(self, item, force, aimed_to) -> str:
        results = ""

        if not self.enemy:
            return results

        damage = 5 if item == self.character.weapon else 2
        agility_req = self.enemy.agility
        strength_req = self.enemy.strength
        intellect_req = self.enemy.intellect

        if force == "light":
            damage *= 0.5
            strength_req -= 1
            intellect_req += 1
        elif force == "normal":
            damage *= 1
            strength_req += 0
            intellect_req -= 1
        elif force == "heavy":
            damage *= 2
            strength_req += 3
            intellect_req -= 3
        else:
            damage *= 1
            strength_req += 0

        if aimed_to == "body":
            damage *= 1
            agility_req += 0
        elif aimed_to == "hands":
            damage *= 0.5
            agility_req += 2
        elif aimed_to == "legs":
            damage *= 0.7
            agility_req += 1
        elif aimed_to == "head":
            damage *= 3
            agility_req += 5
        elif aimed_to == "eyes":
            damage *= 1.5
            agility_req += 4
        elif aimed_to == "back":
            damage *= 1.5
            agility_req += 3
        else:
            damage *= 1
            agility_req += 0

        damage += random.randint(-2, 2)
        damage = int(damage)

        agility_req = 1 if agility_req < 1 else agility_req
        strength_req = 1 if strength_req < 1 else strength_req
        intellect_req = 1 if intellect_req < 1 else intellect_req

        agility_delta = int(self.character.agility / agility_req * 100) - 100
        strength_delta = int(self.character.strength / strength_req * 100) - 100
        intellect_delta = int(self.character.intellect / intellect_req * 100) - 100
        skills = [agility_delta, strength_delta, intellect_delta]

        #print(f"\n{self.character.agility} / {agility_req} - 100 = {agility_delta}")
        #print(f"\n{self.character.strength} / {strength_req} - 100 = {strength_delta}")
        #print(f"\n{self.character.intellect} / {intellect_req} - 100 = {intellect_delta}")
        #print(f"\nDeye = {deye}")

        sucess, skill = self.__test_attack(skills)

        if skill == 0 and not sucess:
            results += f"\nИгроку не хватило ловкости и {self.enemy.name} увернулся от атаки!"
        elif skill == 1 and not sucess:
            self.enemy.hp -= damage // 2
            results += f"\nИгроку не хватило силы и {self.enemy.name} заблокировал удар!"
            results += f"\n{self.enemy.name} получил урон {damage // 2} вместо {damage}"
        elif skill == 2 and not sucess:
            self.character.hp -= damage // 2
            results += f"\nИгроку не хватило интеллекта и {self.enemy.name} парировал атаку!"
            results += f"\nИгрок получил урон {damage // 2}"
        else:
            self.enemy.hp -= damage
            results += f"\nИгроку нанес успешную атаку по {self.enemy.name}!"
            results += f"\n{self.enemy.name} получил урон {damage}"

        if self.enemy.hp <= 0:
            results += f"\n{self.enemy.name} погиб!"
            return results

        results += f"\n{self.enemy.name} готовиться атаковать!"

        damage = 7
        agility_req = self.character.agility
        strength_req = self.character.strength
        intellect_req = self.character.intellect

        damage += random.randint(-2, 2)
        damage = int(damage)

        agility_req = 1 if agility_req < 1 else agility_req
        strength_req = 1 if strength_req < 1 else strength_req
        intellect_req = 1 if intellect_req < 1 else intellect_req

        agility_delta = int(self.enemy.agility / agility_req * 100) - 100
        strength_delta = int(self.enemy.strength / strength_req * 100) - 100
        intellect_delta = int(self.enemy.intellect / intellect_req * 100) - 100
        skills = [agility_delta, strength_delta, intellect_delta]

        sucess, skill = self.__test_attack(skills)

        if skill == 0 and not sucess:
            results += f"\n{self.enemy.name} не хватило ловкости и игрок увернулся от атаки!"
        elif skill == 1 and not sucess:
            self.character.hp -= damage // 2
            results += f"\n{self.enemy.name} не хватило силы и игрок заблокировал удар!"
            results += f"\nИгрок получил урон {damage // 2} вместо {damage}"
        elif skill == 2 and not sucess:
            self.enemy.hp -= damage // 2
            results += f"\n{self.enemy.name} не хватило интеллекта и игрок парировал атаку!"
            results += f"\n{self.enemy.name} получил урон {damage // 2}"
        else:
            self.character.hp -= damage
            results += f"\n{self.enemy.name} нанес успешную атаку по игроку!"
            results += f"\nИгрок получил урон {damage}"

        if self.enemy.hp <= 0:
            results += f"\n{self.enemy.name} погиб!"
            return results

        return results

    def __test_attack(self, skills: list) -> tuple[bool, int]:
        skill = skills.index(min(skills))
        deye = random.randint(0, 100)

        return deye < 50 + skills[skill], skill
