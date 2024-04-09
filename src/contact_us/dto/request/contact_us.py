from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator

from src.commons.utils.helpers import convert_phone_number_for_db


class ContactUsCreate(BaseModel):
    name: str = Field(
        ...,
        description="Name of the person"
    )
    email: EmailStr = Field(
        ...,
        description="Email-ID of the person"
    )
    phone_number: str = Field(
        ...,
        description="Phone-Number of the person"
    )

    company_name: Optional[str] = Field(
        None,
        description="Company-Name"
    )

    service_id: str = Field(
        ...,
        description="Service-Opted by the person"
    )

    message: Optional[str] = Field(
        None,
        description="Query-Message of the person"
    )

    @field_validator("phone_number")
    def validate_phone_number_format(cls, value):
        if value:
            return convert_phone_number_for_db(value)


class ContactUsDetails(ContactUsCreate):
    id: str = Field(
        ...,
        description="Primary-Key Id of the testimonial"
    )
