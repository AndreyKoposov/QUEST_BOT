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

    def parse(self, player_input: str, targets: list[str], items: list[str]):
        """Парсит ввод от пользователя"""
        query = """
        ## Задача
        Ты — переводчик команд игрока в JSON для текстовой RPG.
        Игрок написал: """ + player_input + """.

        Доступные действия: attack, defend, move, talk, wait, explore, item_use, item_drop.
        Доступные цели: """ + ', '.join([str(t) for t in targets]) + """.
        Доступные предметы: """ + ', '.join([str(i) for i in items]) + """.

        ## Формат ответа
        Проанализируй текст и верни строго валидный JSON по этой схеме:
        [
            {
                "action": (одно из действий),
                "target": (имя цели),
                "item_used": (имя предмета),
                "attack_attrs": {
                    "force": (light/normal/heavy),
                    "aimed_to": (legs/hands/body/head/eyes/back),
                },
                "move_attrs": {
                    "speed": (slow/normal/fast),
                    "stealth": (true/false),
                },
                "defend_attrs": {
                    "type": (block/evasion/parry),
                },
                "talk_attrs": {
                    "type": (friendly/aggressive/neutral),
                    "topic": (тема разговора),
                },
                "wait_attrs": {
                    "time": (время в минутах),
                    "type": (rest/sleep/default),
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


    def summery(self, player_input, results) -> str:
        """Подводит итог действиям игрока и их результатам"""
        query = """
        ## Задача
        Ты — рассказчик-повествователь в текстовой фэнтэзи RPG.
        Игрок написал: """ + player_input + """.
        Результат его действий: """ + results + """.

        ## Формат ответа
        Интересно и в стиле фэнтэзи опиши произошедшие события (1-3 предложения). Обращайся к игроку на Вы.
        Не говори в тексте про очки здоровья и прочие игровые параметры, тебе нужно лишь красиво их интерпретировать.
        """

        return str(self.giga.invoke(query).content)

    def test(self, prev_msg: str, player_input: str, location: str, items: list[tuple[str, int]], effects: list[str], hp: int, money: int, cartridges: int):
        """Парсит ввод от пользователя"""
        query = """
        ## Задача
        Ты — анализатор ввода игрока в JSON для текстовой sci-fi RPG.
        Твоя задача - проанализировать текст, и вернуть JSON, описывающий результат действия игрока.

        Контекст: """ + prev_msg + """.
        Игрок ответил: """ + player_input + """.
        Текущая локация: """ + location + """.
        Текущее здоровье игрока: """ + str(hp) + """ из 100.
        Денег у игрока: """ + str(money) + """.
        Патрон у игрока: """ + str(cartridges) + """.
        Эффекты на игроке: """ + ', '.join([str(e) for e in effects]) + """.
        Предметы у игрока: """ + ', '.join([f"{i}({c})" for i, c in items]) + """.

        ## Формат ответа
        Проанализируй текст и верни строго валидный JSON по этой схеме:
        {
            "feasible": true/false
            "important_skill": (strength/agility/intellect/none),
            "difficult": (easy/normal/hard/none)
            "items": [
                {
                    "item_name": (название предмета),
                    "count": 0,
                    "type": (add/remove/use)
                },
            ],
            "effects": [
                {
                    "effect_name": (название эффекта),
                    "type": (add/remove/use)
                },
            ],
            "location": (имя локации)
            "health_change": 0,
            "money_change": 0,
            "cartridges_change": 0
        }

        ## Правила:
        - Если игрок использует предмет, которого у него нет, или делает иное невыполнимое действие - укажи feasible = false.
        - Укажи какой навык необходим для выполнения действия игрока и сложность исполняемого действия. Если действие обычное или простое - укажи none.
        - Ответ должен содержать ТОЛЬКО JSON, без пояснений.
        - Если игрок не использует предметов - укажи пустой список.
        """

        res = self.giga.invoke(query).content

        if isinstance(res, str):
            Logger.info(f"AI response:\n{res}")
            return res

        Logger.error(f"Bad AI answer:\n{res}")
        return ""
