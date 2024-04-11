from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class Saltoro(BaseModel):
    tagline: str = Field(
        ...,
        description="Tagline of Saltoro"
    )
    brief_introduction: str = Field(
        ...,
        description="Brief Introduction about Saltoro"
    )
    company_introduction: str = Field(
        ...,
        description="Complete Company Introduction"
    )
    about_company: str = Field(
        ...,
        description="About Company"
    )

    address_line_1: str = Field(
        ...,
        description="Company-Address"
    )
    city: str = Field(
        ...,
        description="Company-City"
    )
    state: str = Field(
        ...,
        description="Company-State"
    )
    pincode: str = Field(
        ...,
        description="Company-Pincode"
    )
    country: str = Field(
        ...,
        description="Company-Country"
    )
    phone_number: str = Field(
        ...,
        description="Company Phone-Number"
    )
    email: EmailStr = Field(
        ...,
        description="Company Email"
    )


class SaltoroCreate(Saltoro):
    file_name: str = Field(
        ...,
        description="Logo-File Name"
    )


class SaltoroDetails(Saltoro):
    id: str = Field(
        ...,
        description="Primary-Key Id of the Saltoro-Company"
    )
    logo_url: str = Field(
        ...,
        description="S3 url to access logo"
    )


class SaltoroUpdate(BaseModel):
    tagline: Optional[str] = Field(
        None,
        description="Tagline of Saltoro"
    )
    brief_introduction: Optional[str] = Field(
        None,
        description="Brief Introduction about Saltoro"
    )
    company_introduction: Optional[str] = Field(
        None,
        description="Complete Company Introduction"
    )
    about_company: Optional[str] = Field(
        None,
        description="About Company"
    )

    address_line_1: Optional[str] = Field(
        None,
        description="Company-Address"
    )
    city: Optional[str] = Field(
        None,
        description="Company-City"
    )
    state: Optional[str] = Field(
        None,
        description="Company-State"
    )
    pincode: Optional[str] = Field(
        None,
        description="Company-Pincode"
    )
    country: Optional[str] = Field(
        None,
        description="Company-Country"
    )
    phone_number: Optional[str] = Field(
        None,
        description="Company Phone-Number"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Company Email"
    )

    file_name: Optional[str] = Field(
        None,
        description="Logo-File Name"
    )
