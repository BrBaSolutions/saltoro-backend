import uuid

from sqlalchemy import Column, String, Text, Boolean

from src.strategies.entities.base_model import BaseModel


class Address(BaseModel):
    __tablename__ = "address"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # content
    address_line_1 = Column(Text, nullable=False)

    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    pincode = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)

    phone_number = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
