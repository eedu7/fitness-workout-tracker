import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The user's full name",
        examples=["Uzumaki Naruto"],
    )
    email: EmailStr = Field(
        ...,
        description="The user's email address",
        examples=["uzumaki.naruto@konoha.com"],
    )


class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=128, examples=["Password@123"])

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&#]", value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserLogin(UserBase):
    password: str = Field(..., examples=["Password@123"])


class UserResponse(UserBase):
    id: int = Field(..., examples=[1])

    class Config:
        orm_mode = True


class CurrentUser(BaseModel):
    id: int | None = Field(None, examples=[1])
