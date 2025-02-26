from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import date


class NameBase(BaseModel):
    """Base schema for user's name.

    Attributes:
    title (str): User's title.
    first_name (str): User's first name.
    last_name (str): User's last name.
    """
    title: str = Field(..., json_schema_extra={"example": "Mr"})
    first_name: str = Field(..., json_schema_extra={"example": "John"})
    last_name: str = Field(..., json_schema_extra={"example": "Doe"})

    model_config = ConfigDict(from_attributes=True)


class LoginBase(BaseModel):
    """Base schema for user's login.
    Attributes:
    username (str): User's username.
    role (str): User's role. Default is "user".
    """
    username: str = Field(..., json_schema_extra={"example": "john_doe"})
    role: str = Field(default="user", json_schema_extra={"example": "user"})

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Base schema for user.
    Attributes:
    name (NameBase): User's name.
    login (LoginBase): User's login.
    dob (date): User's date of birth.
    city (str): User's city.
    email (EmailStr): User's email.
    """
    name: NameBase
    login: LoginBase
    dob: date = Field(..., json_schema_extra={"example": "1990-01-01"})
    city: str = Field(..., json_schema_extra={"example": "New York"})
    email: EmailStr = Field(
        ..., json_schema_extra={"example": "john.doe@example.com"}
    )

    model_config = ConfigDict(from_attributes=True)
