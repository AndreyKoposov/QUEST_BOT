from typing import Optional, Awaitable
import redis.asyncio as redis


class RedisDB():
    """Простой класс для работы с Redis"""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self, password: str):
        """Подключение к Redis"""
        self.client = await redis.from_url(
            "redis://localhost:6379",
            password=password,
            decode_responses=True  # Автоматически декодировать ответы в строки
        )

        # Проверяем подключение
        try:
            if await self.aping():
                print("✅ Успешно подключились к Redis")
        except Exception as e:
            print(f"❌ Ошибка подключения к Redis: {e}")
            raise

        return self.client

    async def disconnect(self):
        """Закрытие соединения"""
        if self.client:
            await self.client.aclose()
            print("🔌 Соединение с Redis закрыто")

    async def aping(self) -> bool:
        if self.client is None:
            raise Exception("Сначала нужно подключиться к Redis")

        result = self.client.ping()
        if isinstance(result, Awaitable):
            return await result

        raise Exception("Sync connection to Redis!")
