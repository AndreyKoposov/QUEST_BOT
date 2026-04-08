from vkbottle.bot import Message, BotLabeler

from vk_bot.states import States
from vk_bot.bot import vk


bl = BotLabeler()

@bl.private_message(state=States.WAIT_NAME)
async def name_handler(message: Message):
    name = message.text.strip()

    if len(name) < 3:
        return await message.answer('Имя слишком короткое!')
    if len(name) > 20:
        return await message.answer('Имя слишком длинное!')

    await vk.bot.state_dispenser.set(message.peer_id, States.WAIT_INPUT)
    await message.answer(f"Персонаж создан!\nПривет, {name}!")
