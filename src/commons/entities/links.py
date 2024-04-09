import uuid

from sqlalchemy import Column, String, Text, Boolean

from src.strategies.entities.base_model import BaseModel


class Links(BaseModel):
    __tablename__ = "useful_links"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # content
    name = Column(String(255), nullable=False)
    link = Column(Text, nullable=False)

    # animation s3 key
    logo_key = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
    