from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB():
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    async def connect(self, user: str, pswrd: str, host: str, port: int, db: str):
        """Подключение к MongoDB"""
        # Строка подключения
        connection_string = f"mongodb://{user}:{pswrd}@{host}:{port}"

        # Создаем клиент
        self.client = AsyncIOMotorClient(connection_string)

        # Проверяем подключение
        try:
            await self.client.admin.command('ping')
            print("✅ Успешно подключились к MongoDB")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            raise

        # Выбираем базу данных
        self.db = self.client.get_database(db)
        return self.db

    async def disconnect(self):
        """Закрытие соединения"""
        if self.client:
            self.client.close()
            print("🔌 Соединение с MongoDB закрыто")

    async def get_collection(self, name: str):
        """Получение коллекции"""
        if self.db is None:
            raise Exception("Сначала нужно подключиться к БД")
        return self.db[name]
