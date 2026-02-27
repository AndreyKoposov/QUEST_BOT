"""langchain_gigachat, langchain_core"""
from langchain_gigachat import GigaChat
from app.game.location import Location
from app.utils.logger import Logger
from app.game.action import Action


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

    def parse_action(self, player_input: str, location: Location):
        """Парсит ввод от пользователя"""
        query = \
"""
## Задача
Ты — переводчик текста игрока в JSON для текстовой фэнтэзи RPG.
Нужно определить по тексту какое действие хочет сделать игрок.
Игрок написал: """ + player_input + """.
Локация: """ + location.name + """.
Доступные действия: """ + ', '.join([str(act) for act in location.available_actions()]) + """.

## Формат ответа
Проанализируй текст и верни только строго валидный JSON по этой схеме:
{
    "action": "(одно из действий)"
}

## Правила:
- Не придумывай цели, которых нет в списке.
- Ответ должен содержать ТОЛЬКО JSON, без пояснений.
"""
        print(query)
        res = self.giga.invoke(query).content

        if isinstance(res, str):
            Logger.info(f"AI response:\n{res}")
            return res

        Logger.error(f"Bad AI answer:\n{res}")
        return ""

    def parse_params(self, player_input: str, action: Action, loc: Location):
        """Парсит ввод от пользователя"""
        query = \
"""
## Задача
Ты — анализатор текста игрока в JSON для текстовой фэнтэзи RPG.
Нужно извлечь из текста дополнительную информацию о действии, которое хочет сделать игрок.
Игрок написал: """ + player_input + """.
""" + action.get_context(loc) + """

## Формат ответа
Проанализируй текст и верни строго валидный JSON по этой схеме:
""" + action.get_template() + """
        
## Правила:
- Заполни атрибуты действия.
- Если игрок явно не указал атрибут, пропусти его.
- Не придумывай цели, персонажей и предметы, которых нет в списке. Если игрок сказал "меч", а в списке sword — используй sword.
- Ответ должен содержать ТОЛЬКО JSON, без пояснений.
"""
        print(query)
        res = self.giga.invoke(query).content

        if isinstance(res, str):
            Logger.info(f"AI response:\n{res}")
            return res

        Logger.error(f"Bad AI answer:\n{res}")
        return ""

    def summery(self, player_input: str, context: str) -> str:
        """Подводит итог действиям игрока и их результатам"""
        query = \
"""
## Задача
Ты — рассказчик-повествователь в текстовой фэнтэзи RPG.
Игрок написал: """ + player_input + """.
""" + context + """

## Формат ответа
Интересно и в стиле фэнтэзи опиши произошедшие события и их последствия (2-3 предложения). Обращайся к игроку на Вы.
Не говори в тексте про очки здоровья и прочие игровые параметры, тебе нужно лишь красиво их интерпретировать.
"""
        print(query)
        return str(self.giga.invoke(query).content)
