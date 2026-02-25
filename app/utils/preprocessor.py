"""json, logger"""
from json import loads, JSONDecodeError
from app.utils.logger import Logger


class Preprocessor():
    """Класс для обраотки ответов от ИИ"""
    def __init__(self) -> None:
        self.bad_chars = ['”', '„', '“', '«', '»']

    def preprocess(self, raw_response: str) -> list:
        """Обрабатывает ответ от ИИ"""
        res = self.__select_json(raw_response)
        res = self.__remove_bad_chars(res)
        res = self.__remove_whitespaces(res)
        res = self.__try_parse(res)

        return res

    def __select_json(self, text: str) -> str:
        start = text.find('[')
        end = text.find(']')

        return text[start:end+1]

    def __remove_bad_chars(self, text: str) -> str:
        for bad_char in self.bad_chars:
            text = text.replace(bad_char, '"')

        return text

    def __remove_whitespaces(self, text: str) -> str:
        return "".join(text.split())

    def __try_parse(self, text: str) -> list:
        actions = []

        try:
            actions = loads(text)
        except JSONDecodeError as er:
            Logger.error(f"{er.msg}\nLine: {er.lineno}\nCol: {er.colno}")

        return actions
