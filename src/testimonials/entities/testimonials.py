import uuid

from sqlalchemy import Column, String, Text, Boolean, Numeric

from src.strategies.entities.base_model import BaseModel


class Testimonial(BaseModel):
    __tablename__ = "testimonials"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # testimonial content
    name = Column(String(255), nullable=False)
    rating = Column(Numeric(precision=3, scale=2), nullable=False)
    description = Column(Text, nullable=False)

    # animation s3 key
    logo_key = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
