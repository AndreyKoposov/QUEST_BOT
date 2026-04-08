from typing import Optional, Awaitable
import json
import redis.asyncio as redis


class RedisDB():
    """Простой класс для работы с Redis"""

    def __init__(self):
        self.__client: Optional[redis.Redis] = None

    async def connect(self, password: str) -> redis.Redis:
        """Подключение к Redis"""
        self.__client = await redis.from_url(
            "redis://localhost:6379",
            password=password,
            decode_responses=True  # Автоматически декодировать ответы в строки
        )

        try:
            if await self.__aping():
                print("❤️ Успешно подключились к Redis")
        except Exception as e:
            print(f"❤️ Ошибка подключения к Redis: {e}")
            raise

        return self.__client

    async def disconnect(self):
        """Закрытие соединения"""
        if self.__client:
            await self.__client.aclose()
            print("❤️ Соединение с Redis закрыто")

    async def get(self, peer_id: int) -> tuple[int, dict] | None:
        key = self._make_key(peer_id)
        data = None

        if self.__client:
            data = await self.__client.get(key)

        if data is None:
            return None

        parsed = json.loads(data)
        state = parsed.get("state")
        payload = parsed.get("payload", {})

        return state, payload

    async def set(self, peer_id: int, state: int, **payload):
        key = self._make_key(peer_id)
        data = json.dumps({
            "state": state,
            "payload": payload
        }, default=str)

        if self.__client:
            await self.__client.set(key, data)

    async def delete(self, peer_id: int):
        key = self._make_key(peer_id)
        if self.__client:
            await self.__client.delete(key)

    def _make_key(self, peer_id: int):
        return f'state<{peer_id}>'

    async def __aping(self) -> bool:
        if self.__client is None:
            raise ConnectionError("❤️ Нет подключения к Redis")

        result = self.__client.ping()
        if isinstance(result, Awaitable):
            return await result
        return result

storage = RedisDB()
