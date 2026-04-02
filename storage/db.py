from typing import Optional, Awaitable
import redis.asyncio as redis


class RedisDB():
    """Простой класс для работы с Redis"""

    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self, port: int, password: str) -> redis.Redis:
        """Подключение к Redis"""
        self.client = await redis.from_url(
            f"redis://localhost:{port}",
            password=password,
            decode_responses=True  # Автоматически декодировать ответы в строки
        )

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
            raise ConnectionError("Сначала нужно подключиться к Redis")

        result = self.client.ping()
        if isinstance(result, Awaitable):
            return await result
        return result
