import uuid

from sqlalchemy import Column, String, Text, ForeignKey
from src.commons.config.database import Base


class ContactUs(Base):
    __tablename__ = "contact_us"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # testimonial content
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)

    company_name = Column(String(255), nullable=True)

    # service which user opted for
    service_id = Column(String(36), ForeignKey('services.id'), nullable=True)

    message = Column(Text, nullable=True)
