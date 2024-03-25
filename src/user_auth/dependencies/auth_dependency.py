import json
from datetime import datetime
from typing import Union, Annotated

from fastapi import Depends
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.commons.dependencies.db_dependency import get_db
from src.user_auth.constants.error_codes import ErrorCodes
from src.user_auth.constants.error_messages import ErrorMessages
from src.user_auth.dto.common.schema import TokenPayload
from src.user_auth.dto.request.user import UserDetails
from src.user_auth.exceptions.user_auth_exception import UserAuthException
from src.user_auth.factory.service_factory import ServiceFactory
from src.user_auth.jwt.jwt_dep import JWTBearer
from src.user_auth.jwt.service import JWTService


async def get_current_user(
        token: Annotated[str, Depends(JWTBearer())],
        db: Session = Depends(get_db)
) -> UserDetails:
    try:
        payload = jwt.decode(
            token, JWTService.ACCESS_TOKEN_SECRET_KEY, algorithms=[JWTService.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        json_str = token_data.sub.replace("'", "\"")
        user_token_data = json.loads(json_str)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise UserAuthException(
                error_code=ErrorCodes.EXPIRED_ACCESS_TOKEN,
                error_message=ErrorMessages.EXPIRED_TOKEN
            )
    except(JWTError, ValidationError) as e:
        raise UserAuthException(
            error_code=ErrorCodes.INVALID_ACCESS_TOKEN,
            error_message=ErrorMessages.INVALID_TOKEN,
            error=e
        )

    user: Union[UserDetails, None] = (ServiceFactory.get_user_service(db)
                                      .get_user_by_email(user_token_data['email']))

    return user
