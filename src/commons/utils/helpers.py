import re
from typing import Union, Any

from pydantic import EmailStr
from starlette import status

from src.commons.enum.file_type import FileType
from src.commons.exceptions.saltoro_exception import SaltoroException
from src.commons.utils.logger import Logger

logger = Logger.get_logger()


def handle_db_error(
        at: str,
        error_code: int,
        error_message: str,
        error: Union[Any, None] = None
):
    logger.error(f"{error_code}: {at} due to {error}")

    try:
        error = error.orig.msg
    except:
        error = None

    raise SaltoroException(
        error_code=error_code,
        error_message=error_message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error=error,
    )


def is_valid_phone_number(phone_number: str):
    if not re.match(r"^(\+?0|\+?91)?[6-9]\d{9}$", phone_number, flags=re.IGNORECASE):
        return False
    return True


def convert_phone_number_for_db(phone_number: str):
    if is_valid_phone_number(phone_number):
        if len(phone_number) == 13:
            return phone_number[1:]
        elif len(phone_number) == 12:
            return phone_number
        elif len(phone_number) == 11:
            return "91" + phone_number[1:]
        elif len(phone_number) == 10:
            return "91" + phone_number
    else:
        raise ValueError("Invalid landline number format. Phone number must be 10 digits long.")


def is_valid_password_format(password: str) -> bool:
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
    return re.match(password_pattern, password)


def get_file_key(
        file_type: FileType,
        entity_id: str,
        file_name: str
) -> str:
    print(file_type, entity_id, file_name)
    return "/".join(
        [file_type, entity_id, file_name]
    )


def create_send_contact_us_form_email_template_data(
        name: str,
        email: EmailStr,
        phone_number: str,
        company_name: str,
        service: str,
        query: str
):
    return {
        'userName': name,
        'userEmail': email,
        'userPhone': phone_number,
        'userCompany': company_name,
        'service': service,
        'query': query
    }
