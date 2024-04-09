from _decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class Testimonial(BaseModel):
    name: str = Field(
        ...,
        description="Name of the testimonial"
    )
    rating: Decimal = Field(
        ...,
        description="Rating given by the company"
    )
    description: str = Field(
        ...,
        description="Review description"
    )


class TestimonialCreate(Testimonial):
    file_name: str = Field(
        ...,
        description="Logo-File Name"
    )


class TestimonialDetails(Testimonial):
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
        description="Is-Testimonial still active?"
    )


class TestimonialUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Name of the testimonial"
    )
    rating: Optional[Decimal] = Field(
        None,
        description="Rating given by the company"
    )
    description: Optional[str] = Field(
        None,
        description="Review description"
    )

    file_name: Optional[str] = Field(
        None,
        description="Logo-File Name"
    )
