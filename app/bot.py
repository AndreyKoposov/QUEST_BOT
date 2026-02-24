from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import (Message, InlineKeyboardButton, 
                           InlineKeyboardMarkup, ReplyKeyboardMarkup, 
                           ReplyKeyboardRemove, KeyboardButton)
from dotenv import load_dotenv
from os import getenv
from ai import AI
from game import Game
from preprocessor import Preprocessor
from logger import Logger


# Переменные окружения
load_dotenv()
ROOT = str(getenv('ROOT'))
TOKEN = str(getenv('BOT_TOKEN'))
AUTH = str(getenv('AI_AUTH'))

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Вспомогательные классы
Logger.start(ROOT)
ai = AI(AUTH)
game = Game()
pr = Preprocessor()

current_options = list[str]()

def create_menu(options: list[str]) -> ReplyKeyboardMarkup:
    """Создает меню"""
    buttons = [[KeyboardButton(text=op)] for op in options]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Ваши действия..."
    )
    return keyboard

@dp.message(Command('start'))
async def cmd_start(message: Message):
    """Точка входа"""
    game.start()

    options = game.get_menu()
    keyboard = create_menu(options)
    await message.reply("Привет, это РПГ игра с участием ИИ.", reply_markup=keyboard)
    await message.reply(f"\nТекущая локация: {game.location.name}\n{game.location.desc}")

@router.message(F.text)
async def input_handler(message: Message):
    """Обработчик сообщения от пользователя"""
    if message.text:
        player_input = message.text.strip()[:150]
    else:
        await message.answer("Error")
        return

    if player_input in game.get_menu():
        res = game.do_option(player_input)
    else:
        response = ai.parse_action(player_input, game.location)
        action = pr.preprocess(response)[0]["action"]
        res = game.do_action(action)

    await message.answer(res)

    if game.new_loc:
        options = game.get_menu()
        keyboard = create_menu(options)
        await message.reply(f"\nТекущая локация: {game.location.name}\n{game.location.desc}", reply_markup=keyboard)
    #response = ai.summery(player_input, res)
#
    #await message.answer(res)
    #await message.answer(response)
    #await message.answer(str(game.fight_info()))


if __name__ == '__main__':
    dp.run_polling(bot)
