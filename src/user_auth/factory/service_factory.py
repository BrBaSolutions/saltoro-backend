from sqlalchemy.orm import Session

from src.user_auth.service.user_service import UserService


class ServiceFactory:
    @staticmethod
    def get_user_service(db: Session) -> UserService:
        return UserService(db=db)
