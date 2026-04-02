from vkbottle.bot import Message

from vk_bot.bot import bot


@bot.on.private_message(text='/help')
async def help_(message: Message):
    await message.answer(
        "Доступные команды:"
        "\n\t/start - создать персонажа и начать игру"
        "\n\t/account - информация об аккаунте"
        "\n\t/reset - перезапустить бота"
        "\n\t/about - о боте"
        "\n\t/delete - удалить аккаунт"
    )

@bot.on.private_message(text='/start')
async def start(message: Message):
    pass

@bot.on.private_message(text='/account')
async def account(message: Message):
    pass

@bot.on.private_message(text='/reset')
async def reset(message: Message):
    pass

@bot.on.private_message(text='/about')
async def about(message: Message):
    pass

@bot.on.private_message(text='/delete')
async def delete(message: Message):
    pass
