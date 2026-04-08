from vkbottle.bot import Message, BotLabeler

from mongo.collections import User
from mongo.db import mongo
from storage.db import storage


bl = BotLabeler()

@bl.private_message(text='/help')
async def help_(message: Message):
    await message.answer(
        "Доступные команды:"
        "\n\t/start - создать персонажа и начать игру"
        "\n\t/account - информация об аккаунте"
        "\n\t/reset - перезапустить бота"
        "\n\t/about - о боте"
        "\n\t/delete - удалить аккаунт"
    )

@bl.private_message(text='/start')
async def start(message: Message):
    peer_id = message.peer_id
    user = await mongo.get(User, peer_id)
    if user:
        await message.answer("Аккаунт уже создан!")
    else:
        user = User(peer_id)
        await mongo.create(User, user)
        await message.answer("Аккаунт успешно создан! Давай теперь создадим твоего персонажа.\
                             Введи имя своего персонажа!")

@bl.private_message(text='/account')
async def account(message: Message):
    peer_id = message.peer_id
    user = await mongo.get(User, peer_id)
    if user:
        await message.answer(f'id: {user.peer_id}\n💎 {user.diamonds}\nLogin at: {user.created_at}')
    else:
        await message.answer("Вы ещё не создали аккаунт!")

@bl.private_message(text='/reset')
async def reset(message: Message):
    await storage.delete(message.peer_id)
    await message.answer("Бот перезагрузился!")

@bl.private_message(text='/about')
async def about(message: Message):
    await message.answer("Это игра-бот в жанре текстовый квест с участием ИИ.\
                         Начние игру и пишите что угодно, а мир вам ответит!")

@bl.private_message(text='/delete')
async def delete(message: Message):
    peer_id = message.peer_id
    await mongo.delete(User, peer_id)
    await message.answer("Аккаунт успешно удалён!")
