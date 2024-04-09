import uuid

from sqlalchemy import Column, String, Boolean, Enum

from src.company_relationships.enum.company_relationship_types import CompanyRelationshipTypes
from src.strategies.entities.base_model import BaseModel


class CompanyRelationships(BaseModel):
    __tablename__ = "company_relationships"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # content
    name = Column(String(255), nullable=False)
    company_relationship_type = Column(Enum(CompanyRelationshipTypes), nullable=False)

    # animation s3 key
    logo_key = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)
