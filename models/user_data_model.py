from pydantic import BaseModel, Field, field_validator
from venv import logger
from enum import Enum
from typing import Optional
import datetime


class UserRoles(str, Enum):
    admin = "ADMIN"
    user = "USER"
    super_admin = "SUPER_ADMIN"

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=8, description="Пароль пользователя")
    passwordRepeat: str = Field(..., min_length=8, description="Повтор пароля пользователя")
    roles: list[UserRoles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    @field_validator('email')
    def check_email_for_at(cls, value: str) -> str:
        if not "@"  in value:
            raise ValueError("email должен содержать символ '@'")
        return value

class RegisterUserResponse(BaseModel):
    id: str = Field(min_length=1)
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: list[UserRoles]
    createdAt: str

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value

class LoginUser(BaseModel):
    id: str = Field(min_length=1)
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[UserRoles]

class LoginUserResponse(BaseModel):
    user: LoginUser
    accessToken: str
    refreshToken: str
    expiresIn: int

class LoginData(BaseModel):
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=8, description="Пароль пользователя")


class FullNameUser(BaseModel):
    fullName: str
