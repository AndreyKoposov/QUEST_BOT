from vkbottle import PhotoMessageUploader, Keyboard, Text, LoopWrapper
from vkbottle.bot import Bot, BotLabeler

from vk_bot import VK_TOKEN, M_USER, M_PSWRD, M_DB, R_PSWRD
from vk_bot import RedisStateDispenser
from core.mongo import mongo
from core.shared import storage


class VKBot:
    def __init__(self):
        self.bot = Bot(token=VK_TOKEN)
        self.uploader = PhotoMessageUploader(self.bot.api)
        self.bot.state_dispenser = RedisStateDispenser(storage)

        self.__setup_loop_wrapper()

    def run(self):
        self.bot.loop_wrapper.run()

    def build_keyboard(self, btns: list[list[str]]) -> str:
        kb = Keyboard()
        for row in btns:
            for btn in row:
                kb.add(Text(btn))
            kb.row()
        return kb.get_json()

    def set_labelers(self, labelers: list[BotLabeler]):
        for labeler in labelers:
            self.bot.labeler.load(labeler)

    def __setup_loop_wrapper(self):
        lw = LoopWrapper()
        lw.on_startup.append(self.__startup_task())
        lw.add_task(self.__main_task())
        lw.on_shutdown.append(self.__shutdown_task())

        self.bot.loop_wrapper = lw

    async def __startup_task(self):
        print("Bot started")
        await mongo.connect(M_USER, M_PSWRD, M_DB)
        await storage.connect(R_PSWRD)

    async def __main_task(self):
        await self.bot.run_polling()

    async def __shutdown_task(self):
        await storage.disconnect()
        await mongo.disconnect()
        print("Bot stoped")

vk = VKBot()
