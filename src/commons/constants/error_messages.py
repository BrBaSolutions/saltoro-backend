from enum import Enum


class ErrorMessages(str, Enum):
    # DB Errors
    DB_EXECUTION_ERROR = ("An unexpected error occurred on the server. Please try again later or contact support if "
                          "the problem persists.")
