from fast_python_api.chemas.base import UserBase, NameBase, LoginBase
from datetime import datetime, date
from pydantic import EmailStr
from pydantic.fields import Field
from uuid import UUID


class LoginPublic(LoginBase):
    """Public representation of login details."""
    uuid: UUID = Field(
        ...,
        json_schema_extra={"example": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
    )


class UserPublic(UserBase):
    """Public representation of user details."""
    login: LoginPublic
    created_at: datetime = Field(
        json_schema_extra={"example": datetime.now().isoformat()}
    )


class NameCreate(NameBase):
    """Schema for creating a new name."""
    title: str = Field(json_schema_extra={"example": "Mr"})
    first_name: str = Field(json_schema_extra={"example": "John"})
    last_name: str = Field(json_schema_extra={"example": "Doe"})


class LoginCreate(LoginBase):
    """Schema for creating a new login."""
    password: str = Field(
        json_schema_extra={"example": "my_secret_password"}
    )


class UserCreate(UserBase):
    """Schema for creating a new user."""
    email: EmailStr = Field(
        json_schema_extra={"example": "john.doe@example.com"}
    )
    dob: date = Field(
        json_schema_extra={
            "example": date(1990, 1, 1).isoformat()
        }
    )
    city: str = Field(json_schema_extra={"example": "New York"})
    name: NameCreate
    login: LoginCreate


class NameUpdate(NameBase):
    """Schema for updating name details."""
    title: str | None = Field(
        default=None, json_schema_extra={"example": "Mr"}
    )
    first_name: str | None = Field(
        default=None, json_schema_extra={"example": "John"}
    )
    last_name: str | None = Field(
        default=None, json_schema_extra={"example": "Doe"}
    )


class LoginUpdate(LoginBase):
    """Schema for updating login details."""
    username: str | None = Field(
        default=None, json_schema_extra={"example": "john_doe"}
    )
    password: str | None = Field(
        default=None, json_schema_extra={"example": "my_secret_password"}
    )


class UserUpdate(UserBase):
    """Schema for updating user details."""
    email: EmailStr | None = Field(
        default=None, json_schema_extra={"example": "john.doe@example.com"}
    )
    city: str | None = Field(
        default=None, json_schema_extra={"example": "New York"}
    )
    dob: date | None = Field(
        default=None, json_schema_extra={
            "example": date(1990, 1, 1).isoformat()
        }
    )
    name: NameUpdate | None = None
    login: LoginUpdate | None = None
