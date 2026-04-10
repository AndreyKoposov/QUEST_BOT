from abc import abstractmethod
import asyncio
import functools

from .config import ENGINE, API_KEY, MODEL, TEMP
# from src.app.ai.prompts import p_entities, p_stages, p_transitions, p_params
from .preprocessor import Preprocessor


class AIEngine():
    def __init__(self, max_pool: int = 10) -> None:
        self.semaphore = asyncio.Semaphore(max_pool)
        self.parser = Preprocessor()

    @abstractmethod
    async def chat(self, query: str) -> str:
        pass

    async def extract_action(self, text: str):
        raw_json = await self.chat(text)
        return self.parser.preprocess(raw_json)

    @staticmethod
    def with_semaphore(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            async with self.semaphore:
                result = await func(self, *args, **kwargs)
            return result
        return wrapper

    @staticmethod
    def get_engine() -> 'AIEngine':
        match ENGINE:
            case 'GigaChat':
                from .engines import gigachat
                return gigachat.GigaChatEngine(API_KEY, MODEL, TEMP)
            case _:
                raise ValueError("Unknown AI engine!")
