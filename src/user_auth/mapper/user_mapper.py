from src.user_auth.dto.request.user import UserCreate, UserDetails
from src.user_auth.entities.user import User as UserEntity


class UserMapper:
    @staticmethod
    def user_entity_to_dto(user: UserEntity) -> UserDetails:
        return UserDetails(**user.__dict__)

    @staticmethod
    def user_dto_to_entity(user: UserCreate) -> UserEntity:
        return UserEntity(**user.model_dump())
