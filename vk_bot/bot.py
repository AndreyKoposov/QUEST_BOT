from vkbottle import PhotoMessageUploader, Keyboard, Text, LoopWrapper
from vkbottle.bot import Bot

from vk_bot.routes import labelers
from vk_bot.config import VK_TOKEN, M_USER, M_PSWRD, M_DB, R_PSWRD
from vk_bot.redis_dispenser import RedisStateDispenser
from mongo.db import mongo
from storage.db import storage


class VKBot:
    def __init__(self):
        self.bot = Bot(token=VK_TOKEN)
        self.mongo = mongo
        self.storage = storage
        self.uploader = PhotoMessageUploader(self.bot.api)
        self.bot.state_dispenser = RedisStateDispenser(self.storage)

        self.__set_loop_wrapper()
        self.__set_labelers()

    def run(self):
        self.bot.loop_wrapper.run()

    def build_keyboard(self, btns: list[list[str]]) -> str:
        kb = Keyboard()
        for row in btns:
            for btn in row:
                kb.add(Text(btn))
            kb.row()
        return kb.get_json()

    def __set_loop_wrapper(self):
        lw = LoopWrapper()
        lw.on_startup.append(self.__startup_task())
        lw.add_task(self.__main_task())
        lw.on_shutdown.append(self.__shutdown_task())

        self.bot.loop_wrapper = lw

    def __set_labelers(self):
        for labeler in labelers:
            self.bot.labeler.load(labeler)

    async def __startup_task(self):
        print("Bot started")
        await self.mongo.connect(M_USER, M_PSWRD, M_DB)
        await self.storage.connect(R_PSWRD)

    async def __main_task(self):
        await self.bot.run_polling()

    async def __shutdown_task(self):
        await self.storage.disconnect()
        await self.mongo.disconnect()
        print("Bot stoped")

vk = VKBot()
