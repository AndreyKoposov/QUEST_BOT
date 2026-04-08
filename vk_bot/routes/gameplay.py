from vkbottle.bot import BotLabeler, Message

from vk_bot.config import BASE_DIR
from vk_bot.states import States
from vk_bot.bot import vk
from core.game.session import GameSession


bl = BotLabeler()

@bl.message(state=States.WAIT_INPUT)
async def input_handler(message: Message):
    await vk.bot.state_dispenser.set(message.peer_id, States.BLOCKED)

    session = GameSession()
    msgs, btns, image = await session.process(message.text)
    await message.answer(msgs[0],
                         keyboard=vk.build_keyboard(btns),
                         attachment=await vk.uploader.upload(
                            str(BASE_DIR / f'assets/media/{image}')
                        ))

    await vk.bot.state_dispenser.set(message.peer_id, States.WAIT_INPUT)

@bl.message(state=States.BLOCKED)
async def blocked_handler(message: Message):
    await message.answer('Ваше сообщение обрабатывается, подождите!')
