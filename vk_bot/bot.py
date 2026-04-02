from vkbottle import PhotoMessageUploader, Keyboard, Text, LoopWrapper
from vkbottle.bot import Bot, Message

from vk_bot.config import VK_TOKEN, BASE_DIR, MONGO_USER, MONGO_PSWRD, MONGO_HOST, MONGO_PORT, MONGO_DB
from vk_bot.redis_dispenser import RedisStateDispenser
from vk_bot.states import States
from core.game.session import GameSession
from mongo.db import MongoDB
from redis_storage.db import RedisDB


redis = RedisDB()
bot = Bot(token=VK_TOKEN)
photo_uploader = PhotoMessageUploader(bot.api)

@bot.on.message(text='/create_character')
async def create_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.WAIT_NAME)
    await message.answer("Введите имя вашего персонажа")

@bot.on.message(state=States.WAIT_NAME)
async def name_handler(message: Message):
    name = message.text.strip()

    if len(name) < 3:
        return await message.answer('Имя слишком короткое!')
    if len(name) > 12:
        return await message.answer('Имя слишком длинное!')

    await bot.state_dispenser.set(message.peer_id, States.WAIT_INPUT)
    await create_user(name)
    await message.answer(f"Персонаж создан!\nПривет, {name}!")

@bot.on.message(state=States.WAIT_INPUT)
async def input_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, States.BLOCKED)

    session = GameSession()
    msgs, btns, image = await session.process(message.text)
    await message.answer(msgs[0],
                         keyboard=build_keyboard(btns),
                         attachment=await photo_uploader.upload(str(BASE_DIR / f'assets/media/{image}')))

    await bot.state_dispenser.set(message.peer_id, States.WAIT_INPUT)

@bot.on.message(state=States.BLOCKED)
async def blocked_handler(message: Message):
    await message.answer('Ваше сообщение обрабатывается, подождите!')

async def create_user(name: str):
    mongo = MongoDB()
    try:
        # Подключаемся
        await mongo.connect(MONGO_USER, MONGO_PSWRD, MONGO_HOST, MONGO_PORT, MONGO_DB)
        # Получаем коллекцию
        users = await mongo.get_collection("users")
        # Пример вставки
        result = await users.insert_one({
            "name": name,
        })
        print(f"Добавлен документ с id: {result.inserted_id}")
        # Пример чтения
        user = await users.find_one({"name": name})
        print(f"Найден пользователь: {user}")
        # Закрываем соединение
        await mongo.disconnect()
    except Exception as e:
        print(f"Ошибка: {e}")

def build_keyboard(btns: list[list[str]]) -> str:
    kb = Keyboard()
    for row in btns:
        for btn in row:
            kb.add(Text(btn))
        kb.row()
    return kb.get_json()

async def startup_task():
    await redis.connect('1234')
    if redis.client:
        bot.state_dispenser = RedisStateDispenser(redis.client)

async def shutdown_task():
    await redis.disconnect()

async def bot_task():
    await bot.run_polling()

lw = LoopWrapper()
lw.on_startup.append(startup_task())
lw.add_task(bot_task())
lw.on_shutdown.append(shutdown_task())
bot.loop_wrapper = lw

def run():
    print("Bot started...")
    try:
        lw.run()
    except KeyboardInterrupt:
        print("Bot stoped")
