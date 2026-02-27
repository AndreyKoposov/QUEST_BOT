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
ai = GigaAI(AUTH)
Logger.start(ROOT)

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


sessions = dict[int, GameSession]()

@dp.message(Command('start'))
async def cmd_start(message: Message):
    """Точка входа"""
    if message.from_user is None:
        return

    await message.reply("Привет! Это текстовая RPG игра с участием ИИ.")
    user_id = message.from_user.id
    if user_id not in sessions:
        sessions[user_id] = GameSession(ai)

    await reply(message, sessions[user_id].start())

@router.message(F.text)
async def input_handler(message: Message):
    """Обработчик сообщения от пользователя"""
    if message.from_user is None:
        return
    if message.text is None:
        return
    user_id = message.from_user.id

    await reply(message, sessions[user_id].process(message.text))

async def reply(message: Message, answer: tuple[list[str], list[list[str]]]):
    """Отправляет пользователю все сообщения от игры"""
    messages, buttons = answer
    menu = create_menu(buttons)
    for mes in messages:
        await message.reply(mes, reply_markup=menu)

def create_menu(options: list[list[str]]) -> ReplyKeyboardMarkup:
    """Создает меню"""
    buttons = [[KeyboardButton(text=btn) for btn in line] for line in options]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Ваши действия..."
    )
    return keyboard


if __name__ == '__main__':
    dp.run_polling(bot)
