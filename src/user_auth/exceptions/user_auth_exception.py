from typing import Union, Any

from src.commons.exceptions.saltoro_exception import SaltoroException


class UserAuthException(SaltoroException):
    def __init__(self, error_code: int, error_message: str, status_code: int = 401, error: Union[Any, None] = None):
        super().__init__(error_code, error_message, error, status_code)
