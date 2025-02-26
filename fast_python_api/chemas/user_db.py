from fast_python_api.chemas.base import UserBase, LoginBase, NameBase
from pydantic import ConfigDict, Field
from datetime import datetime


class LoginInDB(LoginBase):
    """
    Represents a login in the database.
    Attributes:
        uuid (str): Unique identifier for the login.
        password (str): Password for the login.
    """
    uuid: str = Field(
        ..., json_schema_extra={
            "example": "123e4567-e89b-12d3-a456-426614174000"
        }
    )
    password: str = Field(
        ..., json_schema_extra={"example": "hashed_password"}
    )

    model_config = ConfigDict(from_attributes=True)


class NameInDB(NameBase):
    """
    Represents a name in the database.
    Attributes:
        user_id (str): Unique identifier for the user.
    """
    user_id: str = Field(
        ..., json_schema_extra={
            "example": "123e4567-e89b-12d3-a456-426614174000"
        }
    )


class UserInDB(UserBase):
    """
    Represents a user in the database.
    Attributes:
        id (str): Unique identifier for the user.
        login (LoginInDB): Login information associated with the user.
        created_at (datetime | None): Timestamp when the user was created.
    """
    id: str = Field(
        ..., json_schema_extra={
            "example": "123e4567-e89b-12d3-a456-426614174000"
        }
    )
    login: LoginInDB
    created_at: datetime | None = Field(
        default=None, json_schema_extra={"example": datetime.now()}
    )

    model_config = ConfigDict(from_attributes=True)
