from vkbottle import PhotoMessageUploader, Keyboard, Text, LoopWrapper
from vkbottle.bot import Bot, Message

from vk_bot.config import VK_TOKEN, BASE_DIR, M_USER, M_PSWRD, M_DB, R_PSWRD
from vk_bot.redis_dispenser import RedisStateDispenser
from vk_bot.states import States
from vk_bot.commands import labeler
from core.game.session import GameSession
from mongo.db import mongo
from storage.db import storage


bot = Bot(token=VK_TOKEN)
bot.state_dispenser = RedisStateDispenser(storage)
bot.labeler = labeler
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

def build_keyboard(btns: list[list[str]]) -> str:
    kb = Keyboard()
    for row in btns:
        for btn in row:
            kb.add(Text(btn))
        kb.row()
    return kb.get_json()

async def startup_task():
    # mongo_client = await mongo.connect(MONGO_USER, MONGO_PSWRD, MONGO_HOST, MONGO_PORT, MONGO_DB)
    # redis_client = await redis.connect(REDIS_PORT, REDIS_PSWRD)

    # bot.state_dispenser = RedisStateDispenser(redis_client)
    print("Bot started")
    await mongo.connect(M_USER, M_PSWRD, M_DB)
    await storage.connect(R_PSWRD)

async def bot_task():
    await bot.run_polling()

async def shutdown_task():
    await storage.disconnect()
    await mongo.disconnect()
    print("Bot stoped")

lw = LoopWrapper()
lw.on_startup.append(startup_task())
lw.add_task(bot_task())
lw.on_shutdown.append(shutdown_task())
bot.loop_wrapper = lw

def run():
    lw.run()
