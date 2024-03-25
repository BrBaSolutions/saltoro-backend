from pydantic import BaseModel, Field, EmailStr


class RefreshToken(BaseModel):
    refresh_token: str = Field(..., description="Refresh Token")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="email")
    password: str = Field(..., description="password")
