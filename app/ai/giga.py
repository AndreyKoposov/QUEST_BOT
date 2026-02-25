"""langchain_gigachat, langchain_core"""
from langchain_gigachat import GigaChat
from app.utils.logger import Logger


class GigaAI():
    """Класс для работы с gigachat api"""
    def __init__(self, auth: str, temp: float = 0.0):
        self.giga = GigaChat(
            credentials=auth,
            model="GigaChat",
            verify_ssl_certs=False,
            temperature=temp,
            scope="GIGACHAT_API_PERS",
            timeout=15
        )

    def parse_action(self, player_input: str, location):
        """Парсит ввод от пользователя"""
        query = """
        ## Задача
        Ты — переводчик команд игрока в JSON для текстовой фэнтэзи RPG.
        Игрок написал: """ + player_input + """.
        Локация: """ + location.name + """.
        Доступные действия: """ + ', '.join([str(act) for act in location.actions]) + """.

        ## Формат ответа
        Проанализируй текст и верни только строго валидный JSON по этой схеме:
        [
            {
                "action": "(одно из действий)"
            }
        ]

        ## Правила:
        - Не придумывай цели, которых нет в списке.
        - Ответ должен содержать ТОЛЬКО JSON, без пояснений.
        """

        res = self.giga.invoke(query).content

        if isinstance(res, str):
            Logger.info(f"AI response:\n{res}")
            return res

        Logger.error(f"Bad AI answer:\n{res}")
        return ""

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