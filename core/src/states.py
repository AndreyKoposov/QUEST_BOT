from enum import Enum


class BaseStates(Enum):
    WAIT_NAME = 0
    WAIT_INPUT = 1
    BLOCKED = 2
