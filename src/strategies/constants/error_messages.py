from enum import Enum


class ErrorMessages(str, Enum):
    STRATEGY_NOT_FOUND = "Strategy not found"
    ADD_STRATEGY_FAILED = "More than 4 strategies can't be added"
