from enum import Enum


class ErrorCodes(int, Enum):
    # JWT token errors
    INVALID_ACCESS_TOKEN = 2001
    EXPIRED_ACCESS_TOKEN = 2002

    # Login/Signup errors
    INCORRECT_PASSWORD = 2003
    PASSWORD_CONFIRM_PASSWORD_MISMATCH = 2004
    USER_ALREADY_EXISTS = 2005
    USER_NOT_FOUND = 2006
