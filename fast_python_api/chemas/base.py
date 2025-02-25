from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date


class NameBase(BaseModel):
    """Base schema for user's name."""
    title: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class LoginBase(BaseModel):
    """Base schema for user's login."""
    username: str
    role: str = "user"

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Base schema for user."""
    name: NameBase
    login: LoginBase
    dob: date
    city: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
