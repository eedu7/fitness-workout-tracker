from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., examples=["Uzumaki Naruto"])
    email: EmailStr = Field(..., examples=["uzumaki.naruto@konoha.com"])


class UserRegister(UserBase):
    password: str = Field(..., examples=["Password123"])


class UserLogin(UserBase):
    email: EmailStr = Field(..., examples=["uzumaki.naruto@konoha.com"])
    password: str = Field(..., examples=["Password123"])



class UserResponse(UserBase):
    id: int = Field(..., examples=[1])
