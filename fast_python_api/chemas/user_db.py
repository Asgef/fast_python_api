from fast_python_api.chemas.base import UserBase, LoginBase, NameBase
from pydantic import ConfigDict
from datetime import datetime


class LoginInDB(LoginBase):
    uuid: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class NameInDB(NameBase):
    user_id: str


class UserInDB(UserBase):
    id: str
    login: LoginInDB
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
