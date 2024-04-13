import uuid

from sqlalchemy import Column, String, Text, Boolean

from src.strategies.entities.base_model import BaseModel


class Strategy(BaseModel):
    __tablename__ = "strategies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # content
    heading = Column(String(255), nullable=False)
    sub_heading = Column(Text, nullable=True)
    description = Column(Text, nullable=False)

    # animation s3 key
    asset_key = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
