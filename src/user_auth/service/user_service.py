import json
from typing import Dict

from sqlalchemy.orm import Session
from starlette import status

from src.user_auth.constants.error_codes import ErrorCodes
from src.user_auth.constants.error_messages import ErrorMessages
from src.user_auth.dao.user_dao import UserDao
from src.user_auth.dto.common.schema import TokenPayload
from src.user_auth.dto.common.token import Token
from src.user_auth.dto.request.authentication import UserLogin
from src.user_auth.dto.request.user import UserDetails, UserCreate
from src.user_auth.entities.user import User
from src.user_auth.exceptions.user_auth_exception import UserAuthException
from src.user_auth.jwt.service import JWTService
from src.user_auth.mapper.user_mapper import UserMapper
from src.user_auth.utils.helpers import verify_password


class UserService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.userDao = UserDao(db=db)

    def create_user(self, user: UserCreate) -> UserDetails:
        # Check whether this user already exists or not
        if self.userDao.exists_by_email_or_phone(
                email=user.email,
                phone_number=user.phone_number
        ):
            raise UserAuthException(
                status_code=400,
                error_code=ErrorCodes.USER_ALREADY_EXISTS,
                error_message=ErrorMessages.USER_ALREADY_EXISTS,
            )

        # Create the user entity
        user: User = UserMapper.user_dto_to_entity(user)

        user: User = self.userDao.create_user(
            user=user
        )

        return UserMapper.user_entity_to_dto(user)

    def _get_user_entity_by_email(
            self,
            email: str
    ) -> User:
        user: User = self.userDao.get_user_by_email(email=email)

        if user is None:
            raise UserAuthException(
                error_code=ErrorCodes.USER_NOT_FOUND,
                error_message=ErrorMessages.USER_NOT_FOUND.format(email=email),
                status_code=status.HTTP_404_NOT_FOUND
            )

        return user

    def get_user_by_email(self, email: str) -> UserDetails:
        user: User = self._get_user_entity_by_email(
            email=email
        )

        return UserMapper.user_entity_to_dto(user)

    def user_login(
            self,
            login_request: UserLogin
    ):
        user: User = self._get_user_entity_by_email(
            email=login_request.email
        )

        if not verify_password(login_request.password, user.password):
            raise UserAuthException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INCORRECT_PASSWORD,
                error_message=ErrorMessages.INCORRECT_PASSWORD
            )

        token_payload: Dict = {
            "email": user.email,
            "user_name": user.user_name
        }

        token: Token = Token(
            access_token=JWTService.create_access_token(token_payload),
            refresh_token=JWTService.create_refresh_token(token_payload)
        )

        return token

    def refresh_token(self, refresh_token: str) -> Token:
        payload = JWTService.verify_refresh_token(refresh_token=refresh_token)
        token_data = TokenPayload(**payload)
        json_str = token_data.sub.replace("'", "\"")
        user_token_data = json.loads(json_str)

        email = user_token_data.get("email")

        user: User = self._get_user_entity_by_email(email=email)

        return Token(
            access_token=JWTService.create_access_token(user_token_data),
            refresh_token=refresh_token
        )
