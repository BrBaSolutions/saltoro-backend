from typing import Optional

from pydantic import BaseModel, Field

from src.company_relationships.enum.company_relationship_types import CompanyRelationshipTypes


class CompanyRelationship(BaseModel):
    name: str = Field(
        ...,
        description="Name of the company"
    )
    company_relationship_type: CompanyRelationshipTypes = Field(
        ...,
        description="Relationship with the company"
    )


class CompanyRelationshipCreate(CompanyRelationship):
    file_name: str = Field(
        ...,
        description="Logo-File Name"
    )


class CompanyRelationshipDetails(CompanyRelationship):
    id: str = Field(
        ...,
        description="Primary-Key Id of the testimonial"
    )
    logo_url: str = Field(
        ...,
        description="S3 url to access logo"
    )
    is_active: bool = Field(
        ...,
        description="Is-CompanyRelationship still active?"
    )


class CompanyRelationshipUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Name of the company"
    )
    company_relationship_type: Optional[CompanyRelationshipTypes] = Field(
        None,
        description="Relationship with the company"
    )

    file_name: Optional[str] = Field(
        None,
        description="Logo-File Name"
    )
