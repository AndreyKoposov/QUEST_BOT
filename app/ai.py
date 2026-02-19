"""langchain_gigachat, langchain_core"""
from langchain_gigachat import GigaChat
from logger import Logger


class AI():
    """Класс для работы с gigachat api"""
    def __init__(self, auth: str, temp: float = 0.5):
        self.giga = GigaChat(
            credentials=auth,
            model="GigaChat",
            verify_ssl_certs=False,
            temperature=temp,
            scope="GIGACHAT_API_PERS",
            timeout=15
        )

    def parse(self, player_input: str):
        """Парсит ввод от пользователя"""
        query = """
        ## Задача
        Ты — переводчик команд игрока в JSON для текстовой RPG.
        Игрок написал: """ + player_input + """.

        Доступные действия: attack, defend, move, talk, wait, explore, item_use, item_drop.
        Доступные цели: player, goblin, chest, door, left_room, right_room, hall.
        Доступные предметы: sword, key, torch, health_potion.

        ## Формат ответа
        Проанализируй текст и верни строго валидный JSON по этой схеме:
        [
            {
                "action": (одно из действий),
                "target": (имя цели),
                "item_used": (имя предмета),
                "skill_used": (имя навыка),
                "attack_attrs": {
                    "force": (light/normal/heavy),
                    "aimed_to": (legs/hands/body/head),
                },
                "move_attrs": {
                    "speed": (slow/normal/fast),
                    "stealth": (true/false),
                },
                "talk_attrs": {
                    "type": (friendly/aggressive/neutral),
                    "topic": (тема разговора),
                },
                "wait_attrs": {
                    "time": (время в минутах),
                    "type": (rest/sleep/default),
                },
                "item_use_attrs": {
                    "count": 1.0,
                },
                "item_drop_attrs": {
                    "count": 1.0,
                },
            },
        ]

        ## Правила:
        - Если игрок явно не указал параметр, пропусти его.
        - Заполни атрибуты действия.
        - Не придумывай цели, действия и предметы, которых нет в списке. Если игрок сказал "меч", а в списке sword — используй sword.
        - Ответ должен содержать ТОЛЬКО JSON, без пояснений.
        """

        res = self.giga.invoke(query).content

        if isinstance(res, str):
            Logger.info(f"AI response:\n{res}")
            return res

        Logger.error(f"Bad AI answer:\n{res}")
        return ""


    def summery(self):
        """Подводит итог действиям игрока и их результатам"""
