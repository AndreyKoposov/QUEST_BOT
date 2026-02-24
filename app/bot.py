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

last_response = ""

def get_main_menu() -> ReplyKeyboardMarkup:
    """Создает меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Атака")],
            [KeyboardButton(text="Защита")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Ваш ход"
    )
    return keyboard

@dp.message(Command('start'))
async def cmd_start(message: Message):
    """Точка входа"""
    await message.reply("Привет, это РПГ игра с участием ИИ.", reply_markup=get_main_menu())
    res = game.next_floor()
    await message.reply(res)

@router.message(F.text)
async def custom_action(message: Message):
    """Обработчик сообщения от пользователя"""
    if message.text:
        player_input = message.text.strip()[:150]
    else:
        await message.answer("Error")
        return

    #response = ai.parse(player_input, game.get_targets(), game.get_items())
    #actions = pr.preprocess(response)
    #res = game.act(actions)
    #response = ai.summery(player_input, res)
#
    #await message.answer(res)
    #await message.answer(response)
    #await message.answer(str(game.fight_info()))

    response = ai.test(last_response, player_input, "laboratory", [("lazer_gun", 1), ("first_aid_kit", 1)], ["tiredness"], 100, 10, 10)
    print(response)


if __name__ == '__main__':
    dp.run_polling(bot)
