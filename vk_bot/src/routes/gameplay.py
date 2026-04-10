from vkbottle.bot import BotLabeler, Message

from core.game import GameSession
from ..config import BASE_DIR
from ..states import States
from ..bot import vk


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
