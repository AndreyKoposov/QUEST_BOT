from vk_bot.bot import vk
from vk_bot.routes import labelers


if __name__ == "__main__":
    vk.set_labelers(labelers)
    vk.run()
