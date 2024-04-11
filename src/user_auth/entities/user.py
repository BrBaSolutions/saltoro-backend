import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.event import listens_for

from src.user_auth.entities.base_model import BaseModel
from src.user_auth.utils.helpers import hash_password, generate_username


class User(BaseModel):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, default=None)

    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(255), unique=True, default=None)
    password = Column(String(60), nullable=False)

    is_active = Column(Boolean, default=True)


@listens_for(User, 'before_insert')
def hash_user_password(mapper, connection, target: User):
    if target.password:
        target.password = hash_password(target.password)

    target.user_name = generate_username(target.name)
