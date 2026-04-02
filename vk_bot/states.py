from vkbottle.dispatch import BaseStateGroup


class States(BaseStateGroup):
    WAIT_NAME = 0
    WAIT_INPUT = 1
    BLOCKED = 2
