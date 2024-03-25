from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, ExpiredSignatureError, JWTError

from src.commons.client.config_client import ConfigClient
from src.user_auth.constants.error_codes import ErrorCodes
from src.user_auth.constants.error_messages import ErrorMessages
from src.user_auth.exceptions.user_auth_exception import UserAuthException


class JWTService:
    ALGORITHM = ConfigClient.get_property(section='JWT', name='ALGORITHM')
    ACCESS_TOKEN_SECRET_KEY = ConfigClient.get_property(section='JWT', name='ACCESS_TOKEN_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY = ConfigClient.get_property(section='JWT', name='REFRESH_TOKEN_SECRET_KEY')
    ACCESS_TOKEN_EXPIRY = ConfigClient.get_property(section='JWT', name='ACCESS_TOKEN_EXPIRY')
    REFRESH_TOKEN_EXPIRY = ConfigClient.get_property(section='JWT', name='REFRESH_TOKEN_EXPIRY')

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is None:
            minutes: int = int(JWTService.ACCESS_TOKEN_EXPIRY)
            expires_delta = timedelta(minutes=minutes)

        return JWTService.create_jwt_token(JWTService.ACCESS_TOKEN_SECRET_KEY, subject, expires_delta)

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is None:
            minutes: int = int(JWTService.REFRESH_TOKEN_EXPIRY)
            expires_delta = timedelta(minutes=minutes)

        return JWTService.create_jwt_token(JWTService.REFRESH_TOKEN_SECRET_KEY, subject, expires_delta)

    @staticmethod
    def create_jwt_token(secret_key: str, subject: Union[str, Any], expires_delta: int) -> str:
        expires_delta = datetime.utcnow() + expires_delta
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, secret_key, JWTService.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token,
                JWTService.REFRESH_TOKEN_SECRET_KEY,
                algorithms=[JWTService.ALGORITHM]
            )
            return payload
        except ExpiredSignatureError:
            raise UserAuthException(
                error_code=ErrorCodes.EXPIRED_ACCESS_TOKEN,
                error_message=ErrorMessages.EXPIRED_TOKEN
            )
        except JWTError:
            raise UserAuthException(
                error_code=ErrorCodes.INVALID_ACCESS_TOKEN,
                error_message=ErrorMessages.INVALID_TOKEN
            )

