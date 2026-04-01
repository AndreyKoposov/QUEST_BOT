from dotenv import load_dotenv
from vkbottle.bot import Bot, Message

from vk_bot.config import VK_TOKEN, DEBUG


load_dotenv()
TOKEN = VK_TOKEN
bot = Bot(token=TOKEN)

@bot.on.message(text=["привет", "здравствуй", "хай", "hi", "hello"])
async def greet_handler(message: Message):
    await message.answer("Привет! Я бот этого сообщества 🤖")

@bot.on.message(text=["что ты умеешь", "помощь", "/help"])
async def help_handler(message: Message):
    await message.answer(
        "Я умею:\n"
        "• Отвечать на приветствия\n"
        "• Рассказывать о себе\n"
        "\nНапиши «привет» чтобы начать!"
    )

@bot.on.message()
async def fallback_handler(message: Message):
    await message.answer("Не понял тебя 🤔 Напиши «помощь» чтобы узнать что я умею.")


if __name__ == "__main__":
    if DEBUG:
        print('Run in debug')

    bot.run_forever()
