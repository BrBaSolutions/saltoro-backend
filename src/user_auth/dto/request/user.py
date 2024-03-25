from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator, validator

from src.commons.utils.helpers import convert_phone_number_for_db, is_valid_password_format


class User(BaseModel):
    name: str = Field(..., description="First name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    phone_number: str = Field(..., description="Phone number of the user")

    @field_validator("phone_number")
    def validate_phone_number_format(cls, value):
        if value:
            return convert_phone_number_for_db(value)


class UserCreate(User):
    password: Optional[str] = Field(None, description="Password of the user")

    @validator("password", pre=True, always=True)
    def add_password_if_not(cls, value):
        if not value:
            value = "Saltoro@123"
        return value

    @field_validator("password")
    def validate_password_format(cls, value):
        if value:
            if not is_valid_password_format(password=value):
                raise ValueError(
                    "Password must be at least 8 characters long and contain at least one uppercase letter, "
                    "one lowercase letter, one numeric digit, and one special character.")
        return value


class UserDetails(User):
    id: str = Field(None, description="Id of the user")
    is_active: bool = Field(None, description="This is user's presence.")

