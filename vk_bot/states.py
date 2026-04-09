from vkbottle.dispatch import BaseStateGroup

from core.states import BaseStates


class States(BaseStateGroup):
    WAIT_NAME = BaseStates.WAIT_NAME
    WAIT_INPUT = BaseStates.WAIT_INPUT
    BLOCKED = BaseStates.BLOCKED
