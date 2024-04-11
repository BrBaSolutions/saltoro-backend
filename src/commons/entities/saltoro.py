import uuid

from sqlalchemy import Column, String, Text

from src.strategies.entities.base_model import BaseModel


class Saltoro(BaseModel):
    __tablename__ = "saltoro"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # content
    tagline = Column(Text, nullable=False)
    brief_introduction = Column(Text, nullable=False)

    company_introduction = Column(Text, nullable=False)
    about_company = Column(Text, nullable=False)

    # animation s3 key
    logo_key = Column(String(255), nullable=False)

    # address
    address_line_1 = Column(Text, nullable=False)

    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    pincode = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)

    phone_number = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
