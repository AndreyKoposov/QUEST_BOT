from enum import Enum


class StateID(str, Enum):
    """ID состояний таверны"""
    ENTER = "enter"
    SELECT_GAME = "select_game"
    CARDS_START = "cards_start"
    CARDS_PLAY = "cards_play"
