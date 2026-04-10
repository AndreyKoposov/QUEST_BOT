from vk_bot import vk
from vk_bot import labelers


if __name__ == "__main__":
    vk.set_labelers(labelers)
    vk.run()
