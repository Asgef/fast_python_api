from fast_python_api.chemas.base import UserBase, LoginBase
from pydantic import ConfigDict


class LoginInDB(LoginBase):
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    login: LoginInDB

    model_config = ConfigDict(from_attributes=True)
