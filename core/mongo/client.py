from typing import Optional, Any, Type
from motor.motor_asyncio import AsyncIOMotorClient

from core.mongo.wrapper import Wrapper, T


class MongoDB():
    def __init__(self):
        self.__client: Optional[AsyncIOMotorClient] = None
        self.__db = None

    async def connect(self, user: str, pswrd: str, db: str):
        connection_string = f"mongodb://{user}:{pswrd}@mongo:27017"

        self.__client = AsyncIOMotorClient(connection_string)

        try:
            await self.__client.admin.command('ping')
            print("🌿 Успешное подключение к MongoDB")
        except Exception as e:
            print(f"🌿 Ошибка подключения: {e}")
            raise

        self.__db = self.__client.get_database(db)

    async def disconnect(self):
        if self.__client:
            self.__client.close()
            print("🌿 Соединение с MongoDB закрыто")

    async def get(self, collection: Type[T], obj_id: Any) -> Optional[T]:
        wrap = Wrapper(collection)
        objs = await self.__get_collection(wrap.name)
        obj = await objs.find_one({wrap.key: obj_id})
        return wrap.from_json(obj) if obj else None

    async def create(self, collection: Type[T], obj: T):
        wrap = Wrapper(collection)
        objs = await self.__get_collection(wrap.name)
        await objs.insert_one(wrap.to_json(obj))

    async def update(self, collection: Type[T], obj: T):
        wrap = Wrapper(collection)
        objs = await self.__get_collection(wrap.name)
        serialized = wrap.to_json(obj)
        await objs.update_one({wrap.key: serialized[wrap.key]}, serialized)

    async def delete(self, collection: Type[T], obj_id: Any):
        wrap = Wrapper(collection)
        objs = await self.__get_collection(wrap.name)
        await objs.delete_one({wrap.key: obj_id})

    async def __get_collection(self, name: str):
        """Получение коллекции"""
        if self.__db is None:
            raise ConnectionError("🌿 Нет подключения к базе данных")
        return self.__db[name]

mongo = MongoDB()
