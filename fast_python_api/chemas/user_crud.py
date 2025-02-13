from pydantic import EmailStr
from fast_python_api.chemas.base import UserBase, NameBase, LoginBase
from datetime import datetime, date
import uuid


class LoginPublic(LoginBase):
    uuid: uuid.UUID


class UserPublic(UserBase):
    login: LoginPublic
    created_at: datetime


class NameCreate(NameBase):
    title: str
    first_name: str
    last_name: str


class LoginCreate(LoginBase):
    password: str


class UserCreate(UserBase):
    email: EmailStr
    dob: date
    city: str
    name: NameCreate
    login: LoginCreate
