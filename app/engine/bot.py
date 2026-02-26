"""aiogram, os, dotenv, app"""
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from app.ai.giga import GigaAI
from app.utils.logger import Logger
from app.game.session import GameSession
from app.game.player import Player


# Переменные окружения
load_dotenv()
ROOT = str(getenv('ROOT'))
TOKEN = str(getenv('BOT_TOKEN'))
AUTH = str(getenv('AI_AUTH'))

# Вспомогательные классы
GIGA = GigaAI(AUTH)
Logger.start(ROOT)

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

   
player = Player()
session = GameSession(player, GIGA)

@dp.message(Command('start'))
async def cmd_start(message: Message):
    """Точка входа"""
    await message.reply("Привет! Это текстовая RPG игра с участием ИИ.")
    reply = session.start()

    for mes in reply:
        menu = None
        if mes[1]:
            options = mes[1]
            menu = create_menu(options)
        await message.reply(mes[0], reply_markup=menu)

@router.message(F.text)
async def input_handler(message: Message):
    """Обработчик сообщения от пользователя"""
    if message.text is None:
        return

    reply = session.process_input(message.text)

    for mes in reply:
        menu = None
        if mes[1]:
            options = mes[1]
            menu = create_menu(options)
        await message.reply(mes[0], reply_markup=menu)

def create_menu(options: list[str]) -> ReplyKeyboardMarkup:
    """Создает меню"""
    buttons = [[KeyboardButton(text=op)] for op in options]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Ваши действия..."
    )
    return keyboard

if __name__ == '__main__':
    dp.run_polling(bot)
