from fast_python_api.chemas.base import UserBase, NameBase, LoginBase
from datetime import datetime, date
from pydantic import EmailStr
import uuid


class LoginPublic(LoginBase):
    """Public representation of login details."""
    uuid: uuid.UUID


class UserPublic(UserBase):
    """Public representation of user details."""
    login: LoginPublic
    created_at: datetime


class NameCreate(NameBase):
    """Schema for creating a new name."""
    title: str
    first_name: str
    last_name: str


class LoginCreate(LoginBase):
    """Schema for creating a new login."""
    password: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    email: EmailStr
    dob: date
    city: str
    name: NameCreate
    login: LoginCreate


class NameUpdate(NameBase):
    """Schema for updating name details."""
    title: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class LoginUpdate(LoginBase):
    """Schema for updating login details."""
    username: str | None = None
    password: str | None = None


class UserUpdate(UserBase):
    """Schema for updating user details."""
    email: EmailStr | None = None
    city: str | None = None
    dob: date | None = None
    name: NameUpdate | None = None
    login: LoginUpdate | None = None
