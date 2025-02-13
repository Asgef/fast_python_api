from fast_python_api.chemas.base import UserBase, LoginBase, NameBase
from pydantic import ConfigDict
from datetime import datetime
from uuid import UUID


class LoginInDB(LoginBase):
    uuid: UUID
    password: str

    model_config = ConfigDict(from_attributes=True)


class NameInDB(NameBase):
    user_id: UUID


class UserInDB(UserBase):
    id: UUID
    login: LoginInDB
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
