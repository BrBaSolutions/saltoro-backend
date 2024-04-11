from typing import Optional

from pydantic import BaseModel, Field


class Link(BaseModel):
    name: str = Field(
        ...,
        description="Useful-Link Platform Name"
    )
    link: str = Field(
        ...,
        description="actual link"
    )


class LinkCreate(Link):
    file_name: str = Field(
        ...,
        description="Logo-File Name"
    )


class LinkDetails(Link):
    id: str = Field(
        ...,
        description="Primary-Key Id of the Useful-Link"
    )
    logo_url: str = Field(
        ...,
        description="S3 url to access logo"
    )
    is_active: bool = Field(
        ...,
        description="Is active?"
    )


class LinkUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Useful-Link Platform Name"
    )
    link: Optional[str] = Field(
        None,
        description="actual link"
    )

    file_name: Optional[str] = Field(
        None,
        description="Logo-File Name"
    )
