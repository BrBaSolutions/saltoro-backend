from typing import Optional

from pydantic import BaseModel, Field


class Services(BaseModel):
    heading: str = Field(
        ...,
        description="Title of the strategy"
    )
    sub_heading: Optional[str] = Field(
        None,
        description="Sub-Heading for the strategy"
    )
    description: str = Field(
        ...,
        description="Services description"
    )


class ServicesCreate(Services):
    file_name: str = Field(
        ...,
        description="Asset-File Name"
    )


class ServicesDetails(Services):
    id: str = Field(
        ...,
        description="Primary-Key Id of the testimonial"
    )
    asset_url: str = Field(
        ...,
        description="S3 url to access logo"
    )
    is_active: bool = Field(
        ...,
        description="Is-Services still active?"
    )


class ServicesUpdate(BaseModel):
    heading: Optional[str] = Field(
        None,
        description="Title of the service"
    )
    sub_heading: Optional[str] = Field(
        None,
        description="Sub-Heading for the service"
    )
    description: Optional[str] = Field(
        None,
        description="Services description"
    )

    file_name: Optional[str] = Field(
        None,
        description="Asset-File Name"
    )
