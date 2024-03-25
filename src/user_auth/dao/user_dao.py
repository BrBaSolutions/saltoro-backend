import uuid
from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.commons.constants.error_codes import ErrorCodes
from src.commons.constants.error_messages import ErrorMessages
from src.commons.utils.helpers import handle_db_error
from src.user_auth.entities.user import User


class UserDao:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User, creating_user_id: id = None) -> User:
        try:
            user.id = str(uuid.uuid4())
            if creating_user_id is None:
                creating_user_id = user.id
            user.save(self.db, creating_user_id)
            return user
        except Exception as e:
            handle_db_error(
                "user_auth -> user_dao -> create_user",
                ErrorCodes.DB_EXECUTION_ERROR,
                ErrorMessages.DB_EXECUTION_ERROR,
                e
            )

    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            return self.db.query(User).filter(
                and_(
                    User.email.__eq__(email),
                    User.is_active.__eq__(True)
                )
            ).first()
        except Exception as e:
            handle_db_error(
                "user_auth -> user_dao -> get_user_by_email",
                ErrorCodes.DB_EXECUTION_ERROR,
                ErrorMessages.DB_EXECUTION_ERROR,
                e
            )

    def exists_by_email_or_phone(self, email: str, phone_number: str) -> bool:
        try:
            return (
                    self.db.query(User)
                    .filter(
                        or_(
                            User.email.__eq__(email),
                            User.phone_number.__eq__(phone_number)
                        )
                    )
                    .first()
                    is not None
            )
        except Exception as e:
            handle_db_error(
                "user_auth -> user_dao -> exists_by_email_or_phone",
                ErrorCodes.DB_EXECUTION_ERROR,
                ErrorMessages.DB_EXECUTION_ERROR,
                e
            )
