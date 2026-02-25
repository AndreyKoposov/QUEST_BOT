"""aiogram, os, dotenv, app"""
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from app.ai.giga import GigaAI
from app.utils.preprocessor import Preprocessor
from app.utils.logger import Logger


# Переменные окружения
load_dotenv()
ROOT = str(getenv('ROOT'))
TOKEN = str(getenv('BOT_TOKEN'))
AUTH = str(getenv('AI_AUTH'))

# Вспомогательные классы
GIGA = GigaAI(AUTH)
Logger.start(ROOT)
pr = Preprocessor()

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@dp.message(Command('start'))
async def cmd_start(message: Message):
    """Точка входа"""
    await message.reply("Hello World!")

@router.message(F.text)
async def input_handler(message: Message):
    """Обработчик сообщения от пользователя"""
    if message.text:
        await message.reply(message.text)

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
