from .src.bot import vk
from .src.routes import labelers


if __name__ == "__main__":
    vk.set_labelers(labelers)
    vk.run()
