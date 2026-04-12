from utils import logger
from .src.bot import vk
from .src.routes import labelers


if __name__ == "__main__":
    logger.bind(service='vk_bot')

    vk.set_labelers(labelers)
    vk.run()
